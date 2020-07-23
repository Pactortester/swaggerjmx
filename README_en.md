# swaggerjmx


[![Build Status](https://travis-ci.com/Pactortester/swaggerjmx.svg?branch=master)](https://travis-ci.com/Pactortester/swaggerjmx) ![PyPI](https://img.shields.io/pypi/v/swaggerjmx) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/swaggerjmx) ![GitHub top language](https://img.shields.io/github/languages/top/Pactortester/swaggerjmx) ![PyPI - Downloads](https://img.shields.io/pypi/dm/swaggerjmx?style=plastic) ![GitHub stars](https://img.shields.io/github/stars/Pactortester/swaggerjmx?style=social) ![https://blog.csdn.net/flower_drop](https://img.shields.io/badge/csdn-%40flower__drop-orange)


## Logo

![logo](https://github.com/Pactortester/swaggerjmx/blob/master/images/swaggerjmx.png)


## install


pip install swaggerjmx


##  Warehouse Address：


- github：https://github.com/Pactortester/swaggerjmx.git
- pypi：https://pypi.org/project/swaggerjmx/#history


## Community address


- testerhome：https://testerhome.com/opensource_projects/swaggerjmx


## Applicable scenarios


1. Because interface test scripts are time-consuming to write, and require continuous maintenance, time-consuming and labor-intensive, using this tool can generate interface test scripts with one click.
2. The swagger-ui interface document generates jmx files with one click for use by jmeter.


## Features


1. Convert swagger-ui document to jmx file


## Demo_1
- Can be accessed directly swagger_url (http://ip:port/v2/api-doc) Don’t need to log in, use Demo_1 to convert

```python
# -*- coding: utf-8 -*-

from swaggerjmx.convert import conversion
from swaggerjmx.settings import Settings as ST
#  swagger_url
ST.swagger_url = 'http://ip:port/v2/api-docs'
#  report_path
ST.report_path = 'jmx'
# Start conversion
conversion()

```


## Demo_2
- If you need to log in to access, you can copy the json information on the swagger_url page, save the json file, and use Demo_2 to convert

```python
# -*- coding: utf-8 -*-

from swaggerjmx.convert import conversion
from swaggerjmx.settings import Settings as ST
#  swagger_url_json_path 
ST.swagger_url_json_path = 'test.json'
#  report_path
ST.report_path = 'jmx'
# Start conversion
conversion()

```
## 

The above is an introduction to the basic usage of swaggerjmx.

If you find a bug, or if you have any suggestions for swaggerjmx, welcome [swaggerjmx Issues](https://github.com/Pactortester/swaggerjmx/issues) published, thank you very much for your support. Your feedback and suggestions are very valuable, and I hope your participation can help swaggerjmx do better.
