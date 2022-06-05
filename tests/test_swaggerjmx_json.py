# -*- coding: utf-8 -*-
from swaggerjmx.convert import conversion
from swaggerjmx.settings import Settings as ST

# swagger or yapi json
ST.swagger_url_json_path = './data/swagger.json'
#  report_path
ST.report_path = 'jmx'
# 开始转换
conversion()
