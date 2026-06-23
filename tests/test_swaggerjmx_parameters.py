import json
import os

from swaggerjmx.get_swagger import get_test_plan
from swaggerjmx import to_jmx


def test_swagger2_parameters_are_classified():
    result, title = get_test_plan(swagger_json=_petstore_json())

    assert title == "Swagger*Petstore"
    assert _sample(result, "Add a new pet to the store")["raw_body"]["id"] == 1
    assert _sample(result, "Add a new pet to the store")["raw_body"]["name"] == "doggie"
    assert _sample(result, "Finds Pets by status")["query_params"] == {
        "status": "${status}"
    }
    assert _sample(result, "Find pet by ID")["path_params"] == {"petId": "${petId}"}
    assert _sample(result, "Deletes a pet")["header_params"] == {
        "api_key": "${api_key}"
    }
    assert _sample(result, "Updates a pet in the store with form data")[
        "form_params"
    ] == {"name": "test", "status": "test"}
    upload_sample = _sample(result, "uploads an image")
    assert upload_sample["form_params"]["file"] == "test-file"
    assert upload_sample["multipart"] is True


def test_openapi3_parameters_are_classified():
    result, title = get_test_plan(swagger_json=_openapi3_json())

    sample = _sample(result, "Update pet")
    assert title == "OpenAPI Petstore"
    assert sample["path"] == "/v1/pets/{petId}"
    assert sample["path_params"] == {"petId": "${petId}"}
    assert sample["query_params"] == {"includeDetails": "${includeDetails}"}
    assert sample["header_params"] == {"x-trace-id": "${x-trace-id}"}
    assert sample["raw_body"] == {
        "name": "Fluffy",
        "status": "available",
        "age": 3,
        "score": 1.0,
        "active": True,
        "birthday": "2024-01-01",
        "createdAt": "2024-01-01T00:00:00Z",
        "tags": ["test"],
        "owner": {"email": "test"},
    }
    assert sample["content_type"] == "application/json"

    form_sample = _sample(result, "Create pet form")
    assert form_sample["form_params"] == {"name": "form-pet", "status": "available"}
    assert form_sample["content_type"] == "application/x-www-form-urlencoded"


def test_query_params_are_written_as_jmeter_arguments():
    sample = _sample(_petstore_result(), "Finds Pets by status")
    root = _render_sample(sample)

    assert "status" in _values(root, "Argument.name")
    assert "${status}" in _values(root, "Argument.value")
    assert "true" not in _values(root, "HTTPSampler.postBodyRaw")


def test_body_params_are_written_as_raw_json_with_content_type():
    sample = _sample(_petstore_result(), "Add a new pet to the store")
    root = _render_sample(sample)

    assert "true" in _values(root, "HTTPSampler.postBodyRaw")
    assert '"name": "doggie"' in _values(root, "Argument.value")[0]
    assert "${name}" not in _values(root, "Argument.value")[0]
    assert "Content-Type" in _values(root, "Header.name")
    assert "application/json" in _values(root, "Header.value")


def test_path_and_header_params_are_written_to_path_and_header_manager():
    sample = _sample(_petstore_result(), "Deletes a pet")
    root = _render_sample(sample)

    assert "${baseUrl}/v2/pet/${petId}" in _values(root, "HTTPSampler.path")
    assert "petId" not in _values(root, "Argument.name")
    assert "api_key" in _values(root, "Header.name")
    assert "${api_key}" in _values(root, "Header.value")


def test_form_file_params_enable_multipart_arguments():
    sample = _sample(_petstore_result(), "uploads an image")
    root = _render_sample(sample)

    assert "true" in _values(root, "HTTPSampler.DO_MULTIPART_POST")
    assert "additionalMetadata" in _values(root, "Argument.name")
    assert "file" in _values(root, "Argument.name")
    assert "test" in _values(root, "Argument.value")
    assert "test-file" in _values(root, "Argument.value")


def _petstore_result():
    result, _ = get_test_plan(swagger_json=_petstore_json())
    return result


def _petstore_json():
    with open(
        os.path.join(os.path.dirname(__file__), "data", "swagger.json"),
        encoding="utf-8",
    ) as f:
        return json.load(f, strict=False)


def _openapi3_json():
    return {
        "openapi": "3.0.0",
        "info": {"title": "OpenAPI Petstore", "version": "1.0.0"},
        "servers": [{"url": "https://api.example.com/v1"}],
        "tags": [{"name": "pet", "description": "Pet endpoints"}],
        "paths": {
            "/pets/{petId}": {
                "put": {
                    "tags": ["pet"],
                    "summary": "Update pet",
                    "parameters": [
                        {
                            "name": "petId",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"},
                        },
                        {
                            "name": "includeDetails",
                            "in": "query",
                            "schema": {"type": "boolean"},
                        },
                        {
                            "name": "x-trace-id",
                            "in": "header",
                            "schema": {"type": "string"},
                        },
                    ],
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Pet"}
                            }
                        }
                    },
                    "responses": {"200": {"description": "ok"}},
                }
            },
            "/pets/form": {
                "post": {
                    "tags": ["pet"],
                    "summary": "Create pet form",
                    "requestBody": {
                        "content": {
                            "application/x-www-form-urlencoded": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "name": {
                                            "type": "string",
                                            "example": "form-pet",
                                        },
                                        "status": {
                                            "type": "string",
                                            "enum": ["available", "sold"],
                                        },
                                    },
                                }
                            }
                        }
                    },
                    "responses": {"200": {"description": "ok"}},
                }
            },
        },
        "components": {
            "schemas": {
                "Pet": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "example": "Fluffy"},
                        "status": {
                            "type": "string",
                            "enum": ["available", "sold"],
                        },
                        "age": {"type": "integer", "default": 3},
                        "score": {"type": "number"},
                        "active": {"type": "boolean"},
                        "birthday": {"type": "string", "format": "date"},
                        "createdAt": {"type": "string", "format": "date-time"},
                        "tags": {"type": "array", "items": {"type": "string"}},
                        "owner": {
                            "type": "object",
                            "properties": {"email": {"type": "string"}},
                        },
                    },
                }
            }
        },
    }


def _sample(result, summary):
    for group in result:
        for sample in group["sample"]:
            if sample["sampler_comments"] == summary:
                return sample
    raise AssertionError("sample not found: " + summary)


def _render_sample(sample):
    root = to_jmx.etree.Element("jmeterTestPlan")
    hash_tree = to_jmx.jmeter_test_plan(root)
    plan = to_jmx.test_plan(hash_tree, "test")
    thread = to_jmx.thread_group(plan)
    to_jmx.controller(thread, [{"name": "api", "description": "", "sample": [sample]}])
    return root


def _values(root, name):
    return [node.text for node in root.xpath(".//*[@name='%s']" % name)]
