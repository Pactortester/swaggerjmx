# -*- coding: utf-8 -*-
# @Time    : 2020/6/30 17:05
# @Author  : 李佳玮
# @Email   : lijiawei@symbio.com
# @File    : get_swagger.py
# @Software: PyCharm

import requests
import json




def get_test_plan(swagger_url=None, swagger_url_json_path=None):


    global data
    if swagger_url is None:
        try:
            with open(swagger_url_json_path, 'r', encoding='utf-8') as f:
                data = json.load(f, strict=False)
        except TypeError:
            raise TypeError('You must pass a swagger_url_json_path parameter!')
    elif swagger_url_json_path is None:
        response = requests.get(swagger_url)
        data = json.loads(response.text, strict=False)
    elif swagger_url is None and swagger_url_json_path is None:
        raise TypeError('You must pass a parameter!')
    elif swagger_url_json_path is not None and swagger_url is not None:
        raise TypeError('Only one parameter can be passed!')

    host = data.get("host")
    base_path = data.get("basePath")
    path = data.get("paths")
    thread_groups = data.get("tags")
    definitions = data.get("definitions")
    for thread_group in thread_groups:
        thread_group['host'] = str(host).split(":")[0]
        thread_group["port"] = str(host).split(":")[1]
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
                                        if model_name in list(definitions.keys()):
                                            model_value = definitions.get(model_name)
                                            for param_name, param_value in model_value.get("properties").items():
                                                parameters[param_name] = "${" + param_name + "}"
                            thread_group['sample'].append(
                                {"path": base_path + path_key, "method": method, "params": parameters,
                                 "sampler_comments": sample_value.get("description")})

    return thread_groups
get_test_plan(swagger_url='http://10.231.132.81:6003/v2/api-docs')