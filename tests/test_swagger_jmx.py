# -*- coding: utf-8 -*-
import os

from swaggerjmx.convert import conversion
from swaggerjmx.settings import Settings as ST

path = os.path.join(os.getcwd(), 'test.json')
ST.swagger_url_json_path = '/home/travis/build/Pactortester/swaggerjmx/tests/test.json'
# ST.swagger_url_json_path = 'test.json'
# ST.swagger_url = 'http://00000:6003/v2/api-docs'
ST.report_path = 'jmx'
conversion()
