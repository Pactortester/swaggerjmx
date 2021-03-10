# -*- coding: utf-8 -*-
import os
import time

from .get_swagger import get_test_plan
from .to_jmx import *
from .settings import Settings as ST


def conversion():
    """

    :return:
    """
    result, file_name = get_test_plan(swagger_url=ST.swagger_url, swagger_url_json_path=ST.swagger_url_json_path,
                                      swagger_json=ST.swagger_json)
    jmeterTestPlan = etree.Element("jmeterTestPlan")
    hashTree = jmeter_test_plan(jmeterTestPlan)
    testPlan = test_plan(hashTree, file_name)
    # Arguments = arguments(testPlan)
    threadGroup = thread_group(testPlan)
    controller(threadGroup, result)
    etree.tostring(jmeterTestPlan, pretty_print=True)
    tree = etree.ElementTree(jmeterTestPlan)
    # now = time.strftime("%Y-%m-%d_%H-%M-%S")
    try:
        if not os.path.exists(ST.report_path):
            os.mkdir(ST.report_path)
        tree.write('{}/jmeter-'.format(ST.report_path) + file_name + '.jmx', pretty_print=True, xml_declaration=True,
                   encoding='utf-8')
        print('swagger convert jmx is success!')
    except FileNotFoundError as e:
        print(e)
        print('swagger convert jmx is fail!')
