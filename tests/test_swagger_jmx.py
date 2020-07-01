# -*- coding: utf-8 -*-

from swaggerjmx.convert import conversion
from swaggerjmx.settings import Settings as ST

ST.swagger_url = 'http://10.231.132.81:6001/v2/api-docs'
ST.report_path = 'jmx'
conversion()
