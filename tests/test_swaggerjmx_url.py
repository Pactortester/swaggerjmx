# -*- coding: utf-8 -*-
from swaggerjmx.convert import conversion
from swaggerjmx.settings import Settings as ST

#  swagger_url
ST.swagger_url = 'https://ip:port/v2/api-docs'
#  report_path
ST.report_path = 'jmx'
# 开始转换
conversion()
