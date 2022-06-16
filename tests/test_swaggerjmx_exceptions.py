# -*- coding: utf-8 -*-
import json
import os

from swaggerjmx.convert import conversion
from swaggerjmx.settings import Settings as ST


def test_swaggerjmx_none_parameter():
    ST.swagger_json = None
    ST.swagger_url_json_path = None
    ST.swagger_url = None
    ST.report_path = 'jmx'
    # 开始转换
    conversion()
    assert True


def test_swaggerjmx_all_parameter():
    with open(os.path.join(str(__file__).replace("test_swaggerjmx_exceptions.py", ""), 'data', 'swagger.json'), 'r',
              encoding='utf-8') as f:
        data = json.load(f, strict=False)
    ST.swagger_json = data
    ST.swagger_url_json_path = os.path.join(str(__file__).replace("test_swaggerjmx_exceptions.py", ""), 'data', 'swagger.json')
    ST.swagger_url = 'https://www.baidu.com/'
    ST.report_path = 'jmx'
    # 开始转换
    conversion()
    assert True


def test_swaggerjmx_file_error():
    ST.swagger_json = None
    ST.swagger_url_json_path = os.path.join(str(__file__).replace("test_swaggerjmx_exceptions.py", ""), 'data', 'swaggers.json')
    ST.swagger_url = None
    ST.report_path = 'jmx'
    # 开始转换
    conversion()
    assert True


def test_swaggerjmx_file_format_error():
    ST.swagger_json = None
    ST.swagger_url_json_path = os.path.join(str(__file__).replace("test_swaggerjmx_exceptions.py", ""), 'data', 'swagger_error.json')
    ST.swagger_url = None
    ST.report_path = 'jmx'
    # 开始转换
    conversion()
    assert True


def test_swaggerjmx_report_error():
    ST.swagger_json = None
    ST.swagger_url_json_path = os.path.join(str(__file__).replace("test_swaggerjmx_exceptions.py", ""), 'data', 'swagger.json')
    ST.swagger_url = None
    ST.report_path = None
    # 开始转换
    conversion()
    assert True
