# -*- coding: utf-8 -*-

"""
Parameter initialization is a global variable by default. When calling the relevant API,
you need to inherit the setting class and set the corresponding parameters.

"""


class Settings(object):
    """
    # swagger_url
    ST.swagger_url = 'https://www.baidu.com/'
    # 报告生成路径
    ST.report_path = 'jmx'
    # 可以传入swagger_url展示的json文件路径
    swagger_url_json_path = None
    # 可以传入swagger_json
    swagger_json = None
    """
    report_path = 'jmx'  # 默认在当前路径生成jmx文件夹
    swagger_url = None
    swagger_url_json_path = None
    swagger_json = None
