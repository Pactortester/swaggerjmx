import json
import os
import sys
from json import JSONDecodeError
from urllib.parse import urlparse

import requests
from loguru import logger


HTTP_METHODS = {"delete", "get", "head", "options", "patch", "post", "put"}
MISSING = object()


def get_test_plan(swagger_url=None, swagger_url_json_path=None, swagger_json=None):
    """

    :param swagger_url:
    :param swagger_url_json_path:
    :param swagger_json:
    :return:
    """
    if swagger_url is None and swagger_url_json_path is None and swagger_json is None:
        raise TypeError("You must pass a parameter!")
    elif (
        swagger_url_json_path is not None
        and swagger_url is not None
        and swagger_json is not None
    ):
        raise TypeError("Only one parameter can be passed!")

    elif swagger_url is not None:
        try:
            response = requests.get(swagger_url)
            data = json.loads(response.text, strict=False)
        except (requests.RequestException, JSONDecodeError):
            logger.error(f"The response value of {swagger_url} is not in json format")
            logger.warning("Please check if you have access rights?")
            logger.warning("Maybe you should use swagger json file to convert!")
            sys.exit(0)

    elif swagger_url_json_path is not None:
        if not os.path.exists(swagger_url_json_path):
            logger.error(
                f"FileNotFoundError: [Errno 2] No such file or directory: '{swagger_url_json_path}'"
            )
            sys.exit(0)
        try:
            with open(swagger_url_json_path, encoding="utf-8") as f:
                data = json.load(f, strict=False)
        except TypeError:
            raise TypeError("You must pass a swagger_url_json_path parameter!")
    elif swagger_json is not None:
        data = swagger_json

    title = data.get("info", {}).get("title", "")
    host, port, base_path = _get_server_info(data)
    path = data.get("paths") or {}
    thread_groups = _get_thread_groups(data, path)
    schemas = _get_schemas(data)

    for thread_group in thread_groups:
        thread_group["host"] = host
        thread_group["port"] = port
        thread_group["sample"] = []
        for path_key, path_value in path.items():
            if not isinstance(path_value, dict):
                continue
            path_parameters = path_value.get("parameters") or []
            for method, sample_value in path_value.items():
                if method not in HTTP_METHODS or not isinstance(sample_value, dict):
                    continue
                if _operation_tag(sample_value) != thread_group.get("name"):
                    continue
                thread_group["sample"].append(
                    _build_sample(
                        base_path,
                        path_key,
                        method,
                        path_parameters,
                        sample_value,
                        schemas,
                        data,
                    )
                )

    return thread_groups, title


def _build_sample(
    base_path, path_key, method, path_parameters, operation, schemas, data
):
    sample = {
        "path": _join_path(base_path, path_key),
        "method": method,
        "query_params": {},
        "path_params": {},
        "header_params": {},
        "form_params": {},
        "body_params": {},
        "raw_body": None,
        "content_type": None,
        "multipart": False,
        "sampler_comments": operation.get("summary"),
    }

    for parameter in list(path_parameters) + list(operation.get("parameters") or []):
        _parse_parameter(parameter, operation, sample, schemas, data)

    _parse_request_body(operation.get("requestBody"), sample, schemas, data)
    sample["params"] = _legacy_params(sample)
    return sample


def _parse_parameter(parameter, operation, sample, schemas, data):
    parameter = _resolve_ref_object(parameter, data)
    if not isinstance(parameter, dict):
        return

    name = parameter.get("name")
    param_in = parameter.get("in")
    if not name and param_in != "body":
        return

    if param_in == "query":
        sample["query_params"][name] = _variable(name)
    elif param_in == "path":
        sample["path_params"][name] = _variable(name)
    elif param_in == "header":
        sample["header_params"][name] = _variable(name)
    elif param_in == "formData":
        sample["form_params"][name] = _schema_to_value(parameter, schemas, data, name)
        if parameter.get("type") == "file":
            sample["multipart"] = True
        sample["content_type"] = _operation_content_type(operation) or (
            "multipart/form-data"
            if sample["multipart"]
            else "application/x-www-form-urlencoded"
        )
    elif param_in == "body":
        body_name = name or "body"
        schema = parameter.get("schema") or _named_schema(body_name, schemas)
        raw_body = _explicit_value(parameter)
        if raw_body is MISSING:
            raw_body = _schema_to_value(schema, schemas, data, body_name)
        sample["raw_body"] = raw_body
        sample["body_params"] = _body_params(raw_body, body_name)
        sample["content_type"] = (
            _operation_content_type(operation) or "application/json"
        )


def _parse_request_body(request_body, sample, schemas, data):
    request_body = _resolve_ref_object(request_body, data)
    if not isinstance(request_body, dict):
        return

    media_type, media = _select_media_type(request_body.get("content") or {})
    if not media_type or not isinstance(media, dict):
        return

    schema = media.get("schema") or {}
    if media_type == "application/x-www-form-urlencoded":
        sample["form_params"].update(_schema_to_params(schema, schemas, data))
        sample["content_type"] = media_type
    elif media_type == "multipart/form-data":
        sample["form_params"].update(_schema_to_params(schema, schemas, data))
        sample["content_type"] = media_type
        sample["multipart"] = True
    else:
        raw_body = _schema_to_value(schema, schemas, data, "body")
        sample["raw_body"] = raw_body
        sample["body_params"] = _body_params(raw_body, "body")
        sample["content_type"] = media_type


def _schema_to_params(schema, schemas, data):
    schema = _resolve_ref_object(schema, data)
    if not isinstance(schema, dict):
        return {}

    properties = schema.get("properties") or {}
    if not properties:
        return {}

    params = {}
    for name, schema in properties.items():
        params[name] = _schema_to_value(schema, schemas, data, name)
    return params


def _schema_to_value(schema, schemas, data, name):
    schema = _resolve_ref_object(schema, data)
    if schema is None:
        schema = _named_schema(name, schemas)
    if not isinstance(schema, dict):
        return "test"

    explicit_value = _explicit_value(schema)
    if explicit_value is not MISSING:
        return explicit_value

    if "allOf" in schema:
        merged = {}
        for item in schema.get("allOf") or []:
            value = _schema_to_value(item, schemas, data, name)
            if isinstance(value, dict):
                merged.update(value)
        if merged:
            return merged

    schema_type = schema.get("type")
    if schema_type == "array":
        return [_schema_to_value(schema.get("items") or {}, schemas, data, name)]

    properties = schema.get("properties") or {}
    if schema_type == "object" or properties:
        return {
            prop_name: _schema_to_value(prop_schema, schemas, data, prop_name)
            for prop_name, prop_schema in properties.items()
        }

    return _fallback_value(schema)


def _explicit_value(schema):
    if not isinstance(schema, dict):
        return MISSING
    for key in ("example", "default"):
        if key in schema:
            return schema.get(key)
    enum_values = schema.get("enum") or []
    if enum_values:
        return enum_values[0]
    return MISSING


def _fallback_value(schema):
    schema_type = schema.get("type")
    schema_format = schema.get("format")

    if schema_type == "integer":
        return 1
    if schema_type == "number":
        return 1.0
    if schema_type == "boolean":
        return True
    if schema_type == "file" or schema_format in ("binary", "byte"):
        return "test-file"
    if schema_format == "date":
        return "2024-01-01"
    if schema_format == "date-time":
        return "2024-01-01T00:00:00Z"
    return "test"


def _body_params(raw_body, name):
    if isinstance(raw_body, dict):
        return raw_body
    return {name: raw_body}


def _legacy_params(sample):
    params = {}
    params.update(sample.get("query_params") or {})
    params.update(sample.get("form_params") or {})
    params.update(sample.get("body_params") or {})
    return params


def _operation_content_type(operation):
    consumes = operation.get("consumes") or []
    if consumes:
        return consumes[0]
    return None


def _select_media_type(content):
    if not isinstance(content, dict) or not content:
        return None, None

    if "application/json" in content:
        return "application/json", content.get("application/json")
    for media_type, media in content.items():
        if media_type.endswith("+json"):
            return media_type, media
    for media_type in ("application/x-www-form-urlencoded", "multipart/form-data"):
        if media_type in content:
            return media_type, content.get(media_type)
    media_type = next(iter(content))
    return media_type, content.get(media_type)


def _get_thread_groups(data, paths):
    tags = data.get("tags") or []
    if isinstance(tags, list) and tags:
        thread_groups = []
        for tag in tags:
            if isinstance(tag, dict):
                thread_groups.append(dict(tag))
            else:
                thread_groups.append({"name": str(tag), "description": ""})
        return thread_groups

    tag_names = []
    for path_value in paths.values():
        if not isinstance(path_value, dict):
            continue
        for method, operation in path_value.items():
            if method not in HTTP_METHODS or not isinstance(operation, dict):
                continue
            tag_name = _operation_tag(operation)
            if tag_name not in tag_names:
                tag_names.append(tag_name)
    return [
        {"name": tag_name, "description": ""} for tag_name in tag_names or ["default"]
    ]


def _operation_tag(operation):
    tags = operation.get("tags") or []
    if tags:
        return tags[0]
    return "default"


def _get_schemas(data):
    schemas = {}
    definitions = data.get("definitions") or {}
    components = data.get("components") or {}
    component_schemas = components.get("schemas") or {}
    schemas.update(definitions)
    schemas.update(component_schemas)
    return schemas


def _named_schema(name, schemas):
    if not name:
        return None
    model_name = name[0].upper() + name[1:]
    return schemas.get(model_name) or schemas.get(name)


def _resolve_ref_object(value, data):
    if isinstance(value, dict) and value.get("$ref"):
        resolved = _resolve_local_ref(value.get("$ref"), data)
        if resolved is not None:
            return resolved
    return value


def _resolve_local_ref(ref, data):
    if not isinstance(ref, str) or not ref.startswith("#/"):
        return None

    value = data
    for part in ref[2:].split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        if not isinstance(value, dict):
            return None
        value = value.get(part)
    return value


def _get_server_info(data):
    host = data.get("host") or ""
    base_path = data.get("basePath", "")
    if host:
        host, port = _split_host(host)
        return host, port, base_path

    servers = data.get("servers") or []
    if not servers:
        return "", "", base_path

    server_url = servers[0].get("url", "") if isinstance(servers[0], dict) else ""
    parsed = urlparse(server_url)
    if parsed.netloc:
        host, port = _split_host(parsed.netloc)
        return host, port, parsed.path or ""
    return "", "", parsed.path or server_url


def _split_host(host):
    host = str(host)
    if ":" not in host:
        return host, ""
    parts = host.rsplit(":", 1)
    return parts[0], parts[1]


def _join_path(base_path, path_key):
    base_path = base_path or ""
    path_key = path_key or ""
    if not base_path:
        return path_key
    if base_path.endswith("/") and path_key.startswith("/"):
        return base_path[:-1] + path_key
    if not base_path.endswith("/") and not path_key.startswith("/"):
        return base_path + "/" + path_key
    return base_path + path_key


def _variable(name):
    return "${" + str(name) + "}"
