import os

from swaggerjmx.convert import conversion
from swaggerjmx.settings import Settings as ST


def test_swaggerjmx_json_file():
    # swagger or yapi json path
    ST.swagger_json = None
    ST.swagger_url = None
    ST.swagger_url_json_path = os.path.join(
        str(__file__).replace("test_swaggerjmx_json_file.py", ""),
        "data",
        "swagger.json",
    )
    #  report_path
    ST.report_path = "jmx"
    # 开始转换
    conversion()
    assert os.path.exists("./jmx/jmeter-Swagger-Petstore.jmx")
