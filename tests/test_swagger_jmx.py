# -*- coding: utf-8 -*-

from swaggerjmx.convert import conversion
from swaggerjmx.settings import Settings as ST
#  swagger_url
# ST.swagger_url = 'http://ip:port/v2/api-docs'
#  report_path
ST.swagger_url_json_path = 'test.json'
ST.report_path = 'jmx'
# 开始转换
conversion()
