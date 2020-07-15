# swaggerjmx


[![Build Status](https://travis-ci.com/Pactortester/swaggerjmx.svg?branch=master)](https://travis-ci.com/Pactortester/swaggerjmx) ![PyPI](https://img.shields.io/pypi/v/swaggerjmx) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/swaggerjmx) ![GitHub top language](https://img.shields.io/github/languages/top/Pactortester/swaggerjmx) ![PyPI - Downloads](https://img.shields.io/pypi/dm/swaggerjmx?style=plastic) ![GitHub stars](https://img.shields.io/github/stars/Pactortester/swaggerjmx?style=social) ![https://blog.csdn.net/flower_drop](https://img.shields.io/badge/csdn-%40flower__drop-orange)


## Logo

![logo](https://github.com/Pactortester/swaggerjmx/blob/master/images/swaggerjmx.png)


## 安装


pip install swaggerjmx


##  仓库地址：


- github：https://github.com/Pactortester/swaggerjmx.git
- pypi：https://pypi.org/project/swaggerjmx/#history


## 社区地址


- testerhome：https://testerhome.com/opensource_projects/swaggerjmx


## 适用场景


1. 由于接口测试脚本编写耗时，而且需要持续维护，耗时耗力，使用此工具可以一键生成接口测试脚本.
2. swagger-ui接口文档一键生成jmx文件供jmeter使用.


## 功能


1. 将swagger-ui文档转换为jmx文件


## Demo_1
- 可以直接访问 swagger_url (http://ip:port/v2/api-doc) 不需要登录的，使用Demo_1方式转换

```python
# -*- coding: utf-8 -*-

from swaggerjmx.convert import conversion
from swaggerjmx.settings import Settings as ST
#  swagger_url
ST.swagger_url = 'http://ip:port/v2/api-docs'
#  report_path
ST.report_path = 'jmx'
# 开始转换
conversion()

```


## Demo_2
- 需要登录才能访问的，可以复制swagger_url页面上的json信息，保存json文件，使用Demo_2方式转换

```python
# -*- coding: utf-8 -*-

from swaggerjmx.convert import conversion
from swaggerjmx.settings import Settings as ST
#  swagger_url_json_path 
ST.swagger_url_json_path = 'test.json'
#  report_path
ST.report_path = 'jmx'
# 开始转换
conversion()

```
## 

以上便是 swaggerjmx 的基本用法介绍。

如果您有发现错误，或者您对 swaggerjmx 有任何建议，欢迎到 [swaggerjmx Issues](https://github.com/Pactortester/swaggerjmx/issues) 发表，非常感谢您的支持。您的反馈和建议非常宝贵，希望您的参与能帮助 swaggerjmx 做得更好。
