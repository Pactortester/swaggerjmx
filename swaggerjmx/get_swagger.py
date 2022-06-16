# -*- coding: utf-8 -*-
import os
import sys
from json import JSONDecodeError

import requests
import json
from loguru import logger


def get_test_plan(swagger_url=None, swagger_url_json_path=None, swagger_json=None):
    """

    :param swagger_url:
    :param swagger_url_json_path:
    :param swagger_json:
    :return:
    """
    global data

    if swagger_url is None and swagger_url_json_path is None and swagger_json is None:
        raise TypeError('You must pass a parameter!')
    elif swagger_url_json_path is not None and swagger_url is not None and swagger_json is not None:
        raise TypeError('Only one parameter can be passed!')

    elif swagger_url is not None:
        response = requests.get(swagger_url)
        try:
            data = json.loads(response.text, strict=False)
        except JSONDecodeError as e:
            logger.error(f"The response value of {swagger_url} is not in json format")
            logger.warning("Please check if you have access rights?")
            logger.warning("Maybe you should use swagger json file to convert!")
            sys.exit(0)

    elif swagger_url_json_path is not None:
        if not os.path.exists(swagger_url_json_path):
            logger.error(f"FileNotFoundError: [Errno 2] No such file or directory: '{swagger_url_json_path}'")
            sys.exit(0)
        try:
            with open(swagger_url_json_path, 'r', encoding='utf-8') as f:
                data = json.load(f, strict=False)
        except TypeError:
            raise TypeError('You must pass a swagger_url_json_path parameter!')
    elif swagger_json is not None:
        data = swagger_json

    title = data.get("info")["title"]
    host = data.get("host")
    base_path = data.get("basePath", '')
    path = data.get("paths")
    thread_groups = data.get("tags")
    definitions = data.get("definitions")
    for thread_group in thread_groups:
        thread_group['host'] = str(host).split(":")[0]
        try:
            thread_group["port"] = str(host).split(":")[1]
        except IndexError:
            # 当url是域名时 端口传空
            thread_group["port"] = ''
        thread_group['sample'] = []
        for path_key, path_value in path.items():
            if isinstance(path_value, dict):
                for method, sample_value in path_value.items():
                    if isinstance(sample_value, dict):
                        if sample_value.get("tags")[0] == thread_group.get("name"):
                            parameters = {}
                            if isinstance(sample_value.get("parameters"), list):
                                if sample_value.get("parameters").__len__() > 1:
                                    for param in sample_value.get("parameters"):
                                        parameters[param.get("name")] = "${" + param.get("name") + "}"
                                else:
                                    for param in sample_value.get("parameters"):
                                        model_name = (param.get("name"))[0].upper() + (param.get("name"))[1:]
                                        # support YApi docs
                                        try:
                                            if model_name in list(definitions.keys()):
                                                model_value = definitions.get(model_name)
                                                for param_name, param_value in model_value.get("properties").items():
                                                    parameters[param_name] = "${" + param_name + "}"
                                        except AttributeError:
                                            pass
                            thread_group['sample'].append(
                                {"path": base_path + path_key, "method": method, "params": parameters,
                                 "sampler_comments": sample_value.get("summary")})

    return thread_groups, title
