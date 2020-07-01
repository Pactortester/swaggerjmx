# -*- coding: utf-8 -*-

from swaggerjmx.convert import conversion
from swaggerjmx.settings import Settings as ST

ST.swagger_url = 'https://www.baidu.com/'
ST.report_path = 'jmx'
conversion()
