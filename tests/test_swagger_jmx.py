# -*- coding: utf-8 -*-

from swaggerjmx.convert import conversion
from swaggerjmx.settings import Settings as ST

# ST.swagger_url = 'http://10.0.0.0:6003/v2/api-docs'
ST.swagger_url_json_path = './test.json'
ST.report_path = 'jmx'
conversion()
