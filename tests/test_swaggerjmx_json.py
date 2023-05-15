import json
import os

from swaggerjmx.convert import conversion
from swaggerjmx.settings import Settings as ST


def test_swaggerjmx_json():
    # swagger or yapi json
    with open(
        os.path.join(
            str(__file__).replace("test_swaggerjmx_json.py", ""), "data", "swagger.json"
        ),
        encoding="utf-8",
    ) as f:
        data = json.load(f, strict=False)
    ST.swagger_json = data
    #  report_path
    ST.swagger_url_json_path = None
    ST.swagger_url = None
    ST.report_path = "jmx"
    # 开始转换
    conversion()
    assert os.path.exists("./jmx/jmeter-Swagger-Petstore.jmx")
