import json

from lxml import etree


def jmeter_test_plan(root_xml):
    """

    :param root_xml:
    :return:
    """
    JmeterTestPlan = root_xml
    JmeterTestPlan.set("version", "1.2")
    JmeterTestPlan.set("properties", "5.0")
    JmeterTestPlan.set("jmeter", "5.4.3")
    return etree.SubElement(JmeterTestPlan, "hashTree")


def test_plan(parent_xml, plan_name):
    """

    :param parent_xml:
    :param plan_name:
    :return:
    """
    testPlan = etree.SubElement(parent_xml, "TestPlan")
    testPlan.set("guiclass", "TestPlanGui")
    testPlan.set("testclass", "TestPlan")
    testPlan.set("testname", plan_name)
    testPlan.set("enabled", "true")
    stringProp = etree.SubElement(testPlan, "stringProp")
    stringProp.set("name", "TestPlan.comments")
    stringProp.text = ""
    boolProp1 = etree.SubElement(testPlan, "boolProp")
    boolProp1.set("name", "TestPlan.functional_mode")
    boolProp1.text = "false"
    boolProp2 = etree.SubElement(testPlan, "boolProp")
    boolProp2.set("name", "TestPlan.tearDown_on_shutdown")
    boolProp2.text = "false"
    boolProp3 = etree.SubElement(testPlan, "boolProp")
    boolProp3.set("name", "TestPlan.serialize_threadgroups")
    boolProp3.text = "true"
    elementProp = etree.SubElement(testPlan, "elementProp")
    elementProp.set("name", "TestPlan.user_defined_variables")
    elementProp.set("elementType", "Arguments")
    elementProp.set("guiclass", "ArgumentsPanel")
    elementProp.set("testclass", "Arguments")
    elementProp.set("testname", "User Defined Variables")
    elementProp.set("enabled", "true")
    collectionProp = etree.SubElement(elementProp, "collectionProp")
    collectionProp.set("name", "Arguments.arguments")
    stringProp2 = etree.SubElement(testPlan, "stringProp")
    stringProp2.set("name", "TestPlan.user_define_classpath")
    stringProp2.text = ""
    return etree.SubElement(parent_xml, "hashTree")


def thread_group(parent_xml):
    """

    :param parent_xml:
    :return:
    """
    theadGroup = etree.SubElement(parent_xml, "ThreadGroup")
    theadGroup.set("guiclass", "ThreadGroupGui")
    theadGroup.set("testclass", "ThreadGroup")
    theadGroup.set("testname", "Thread Group")
    theadGroup.set("enabled", "true")
    stringProp = etree.SubElement(theadGroup, "stringProp")
    stringProp.set("name", "ThreadGroup.on_sample_error")
    stringProp.text = "continue"
    elementProp = etree.SubElement(theadGroup, "elementProp")
    common_api(
        elementProp,
        {
            "name": "ThreadGroup.main_controller",
            "elementType": "LoopController",
            "guiclass": "LoopControlPanel",
            "testclass": "LoopController",
            "testname": "Loop Controller",
            "enabled": "true",
        },
    )
    boolProp = etree.SubElement(elementProp, "boolProp")
    boolProp.set("name", "LoopController.continue_forever")
    boolProp.text = "false"
    stringProp = etree.SubElement(elementProp, "stringProp")
    stringProp.set("name", "LoopController.loops")
    stringProp.text = "1"
    stringProp = etree.SubElement(theadGroup, "stringProp")
    stringProp.set("name", "ThreadGroup.num_threads")
    stringProp.text = "1"
    stringProp = etree.SubElement(theadGroup, "stringProp")
    stringProp.set("name", "ThreadGroup.ramp_time")
    stringProp.text = "1"
    boolProp = etree.SubElement(theadGroup, "boolProp")
    boolProp.set("name", "ThreadGroup.scheduler")
    boolProp.text = "false"
    stringProp = etree.SubElement(theadGroup, "stringProp")
    stringProp.set("name", "ThreadGroup.duration")
    stringProp.text = ""
    stringProp = etree.SubElement(theadGroup, "stringProp")
    stringProp.set("name", "ThreadGroup.delay")
    stringProp.text = ""
    return etree.SubElement(parent_xml, "hashTree")


def arguments(parent_xml):
    """

    :param parent_xml:
    :return:
    """
    Arguments = etree.SubElement(parent_xml, "ThreadGroup")
    Arguments.set("guiclass", "ArgumentsPanel")
    Arguments.set("testclass", "Arguments")
    Arguments.set("testname", "User defined variables")
    Arguments.set("enabled", "true")
    collectionProp = etree.SubElement(Arguments, "collectionProp")
    collectionProp.set("name", "Arguments.arguments")
    return etree.SubElement(parent_xml, "hashTree")


def controller(parent_xml, result):
    """

    :param parent_xml:
    :param result:
    :return:
    """
    for data in result:
        GenericController = etree.SubElement(parent_xml, "GenericController")
        GenericController.set("guiclass", "LogicControllerGui")
        GenericController.set("testclass", "GenericController")
        GenericController.set("testname", data.get("name"))
        GenericController.set("enabled", "true")
        stringProp = etree.SubElement(GenericController, "stringProp")
        stringProp.set("name", "TestPlan.comments")
        stringProp.text = data.get("description")
        shashTree = etree.SubElement(parent_xml, "hashTree")
        for sample in data.get("sample"):
            HTTPSamplerProxy = etree.SubElement(shashTree, "HTTPSamplerProxy")
            sample_path = str(sample.get("path")).replace("//", "/")
            sampler_comments = sample.get("sampler_comments") or ""
            common_api(
                HTTPSamplerProxy,
                {
                    "guiclass": "HttpTestSampleGui",
                    "testclass": "HTTPSamplerProxy",
                    "testname": sampler_comments + "-" + sample_path,
                    "enabled": "true",
                },
            )

            raw_body = _raw_body(sample)
            if raw_body is not None:
                boolProp = etree.SubElement(HTTPSamplerProxy, "boolProp")
                boolProp.set("name", "HTTPSampler.postBodyRaw")
                boolProp.text = "true"

            collectionProp = _arguments(HTTPSamplerProxy)
            if raw_body is not None:
                _http_argument(collectionProp, "", _json_body(raw_body))
            else:
                for name, value in _request_params(sample).items():
                    _http_argument(collectionProp, name, value)

            # host
            stringProp = etree.SubElement(HTTPSamplerProxy, "stringProp")
            stringProp.set("name", "HTTPSampler.domain")
            # stringProp.text = data.get("host")
            stringProp.text = ""

            # port
            stringProp = etree.SubElement(HTTPSamplerProxy, "stringProp")
            stringProp.set("name", "HTTPSampler.port")
            # stringProp.text = data.get("port")
            stringProp.text = ""

            # protocol
            stringProp = etree.SubElement(HTTPSamplerProxy, "stringProp")
            stringProp.set("name", "HTTPSampler.protocol")
            # stringProp.text = "http"
            stringProp.text = ""

            # encoding
            stringProp = etree.SubElement(HTTPSamplerProxy, "stringProp")
            stringProp.set("name", "HTTPSampler.contentEncoding")
            stringProp.text = "UTF-8"

            # path
            stringProp = etree.SubElement(HTTPSamplerProxy, "stringProp")
            stringProp.set("name", "HTTPSampler.path")
            stringProp.text = "${baseUrl}" + str(sample.get("path")).replace(
                "//", "/"
            ).replace("/{", "/${")

            # method
            stringProp = etree.SubElement(HTTPSamplerProxy, "stringProp")
            stringProp.set("name", "HTTPSampler.method")
            stringProp.text = sample.get("method").upper()

            # follow redirects
            boolProp = etree.SubElement(HTTPSamplerProxy, "boolProp")
            boolProp.set("name", "HTTPSampler.follow_redirects")
            boolProp.text = "true"

            # auto redirects
            boolProp = etree.SubElement(HTTPSamplerProxy, "boolProp")
            boolProp.set("name", "HTTPSampler.auto_redirects")
            boolProp.text = "false"

            # use keepalive
            boolProp = etree.SubElement(HTTPSamplerProxy, "boolProp")
            boolProp.set("name", "HTTPSampler.use_keepalive")
            boolProp.text = "true"

            # DO MULTIPART POST
            boolProp = etree.SubElement(HTTPSamplerProxy, "boolProp")
            boolProp.set("name", "HTTPSampler.DO_MULTIPART_POST")
            boolProp.text = "true" if sample.get("multipart") else "false"

            # embedded url re
            stringProp = etree.SubElement(HTTPSamplerProxy, "stringProp")
            stringProp.set("name", "HTTPSampler.embedded_url_re")
            stringProp.text = ""

            # connect timeout
            stringProp = etree.SubElement(HTTPSamplerProxy, "stringProp")
            stringProp.set("name", "HTTPSampler.connect_timeout")
            stringProp.text = ""

            # response timeout
            stringProp = etree.SubElement(HTTPSamplerProxy, "stringProp")
            stringProp.set("name", "HTTPSampler.response_timeout")
            stringProp.text = ""

            # comments
            stringProp = etree.SubElement(HTTPSamplerProxy, "stringProp")
            stringProp.set("name", "TestPlan.comments")
            stringProp.text = sampler_comments
            hash_tree = etree.SubElement(shashTree, "hashTree")
            _header_manager(hash_tree, sample)


def _arguments(parent_xml):
    elementProp = etree.SubElement(parent_xml, "elementProp")
    common_api(
        elementProp,
        {
            "name": "HTTPsampler.Arguments",
            "elementType": "Arguments",
            "guiclass": "HTTPArgumentsPanel",
            "testclass": "Arguments",
            "testname": "User Defined Variables",
            "enabled": "true",
        },
    )
    collectionProp = etree.SubElement(elementProp, "collectionProp")
    collectionProp.set("name", "Arguments.arguments")
    return collectionProp


def _http_argument(parent_xml, name, value):
    elementProp = etree.SubElement(parent_xml, "elementProp")
    elementProp.set("name", name)
    elementProp.set("elementType", "HTTPArgument")

    boolProp = etree.SubElement(elementProp, "boolProp")
    boolProp.set("name", "HTTPArgument.always_encode")
    boolProp.text = "false"

    stringProp = etree.SubElement(elementProp, "stringProp")
    stringProp.set("name", "Argument.value")
    stringProp.text = str(value)

    stringProp = etree.SubElement(elementProp, "stringProp")
    stringProp.set("name", "Argument.metadata")
    stringProp.text = "="

    boolProp = etree.SubElement(elementProp, "boolProp")
    boolProp.set("name", "HTTPArgument.use_equals")
    boolProp.text = "true"

    stringProp = etree.SubElement(elementProp, "stringProp")
    stringProp.set("name", "Argument.name")
    stringProp.text = name


def _request_params(sample):
    if _has_typed_params(sample):
        params = {}
        params.update(sample.get("query_params") or {})
        params.update(sample.get("form_params") or {})
        return params
    return sample.get("params") or {}


def _raw_body(sample):
    if _has_typed_params(sample):
        return sample.get("raw_body")
    params = sample.get("params") or {}
    if params:
        return params
    return None


def _has_typed_params(sample):
    for key in (
        "query_params",
        "path_params",
        "header_params",
        "form_params",
        "body_params",
        "raw_body",
    ):
        if key in sample:
            return True
    return False


def _json_body(raw_body):
    if isinstance(raw_body, (dict, list)):
        return json.dumps(raw_body)
    return raw_body


def _header_manager(parent_xml, sample):
    headers = dict(sample.get("header_params") or {})
    content_type = sample.get("content_type")
    if content_type and not sample.get("multipart"):
        header_names = [header_name.lower() for header_name in headers.keys()]
        if "content-type" not in header_names:
            headers["Content-Type"] = content_type
    if not headers:
        return

    HeaderManager = etree.SubElement(parent_xml, "HeaderManager")
    HeaderManager.set("guiclass", "HeaderPanel")
    HeaderManager.set("testclass", "HeaderManager")
    HeaderManager.set("testname", "HTTP Header Manager")
    HeaderManager.set("enabled", "true")
    collectionProp = etree.SubElement(HeaderManager, "collectionProp")
    collectionProp.set("name", "HeaderManager.headers")
    for name, value in headers.items():
        elementProp = etree.SubElement(collectionProp, "elementProp")
        elementProp.set("name", "")
        elementProp.set("elementType", "Header")
        stringProp = etree.SubElement(elementProp, "stringProp")
        stringProp.set("name", "Header.name")
        stringProp.text = name
        stringProp = etree.SubElement(elementProp, "stringProp")
        stringProp.set("name", "Header.value")
        stringProp.text = value
    etree.SubElement(parent_xml, "hashTree")


def common_api(obj_xml, datas):
    """

    :param obj_xml:
    :param datas:
    :return:
    """
    for key, value in datas.items():
        obj_xml.set(key, value)
