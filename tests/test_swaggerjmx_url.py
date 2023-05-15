import os

from swaggerjmx.convert import conversion
from swaggerjmx.settings import Settings as ST


def test_swaggerjmx_url():
    try:
        #  swagger_url
        ST.swagger_json = None
        ST.swagger_url_json_path = None
        ST.swagger_url = "https://www.baidu.com"
        # 'https://ip:port/v2/api-docs'
        #  report_path
        ST.report_path = "jmx"
        # 开始转换
        conversion()
    except SystemExit:
        assert os.path.exists("./jmx/jmeter-Swagger-Petstore.jmx")
