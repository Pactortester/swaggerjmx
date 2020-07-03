# swagger_jmx


[![Build Status](https://travis-ci.com/Pactortester/swaggerjmx.svg?branch=master)](https://travis-ci.com/Pactortester/swaggerjmx) ![PyPI](https://img.shields.io/pypi/v/swaggerjmx) ![PyPI - Wheel](https://img.shields.io/pypi/wheel/swaggerjmx) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/swaggerjmx) ![GitHub top language](https://img.shields.io/github/languages/top/Pactortester/swaggerjmx) ![GitHub stars](https://img.shields.io/github/stars/Pactortester/swaggerjmx?style=social) ![https://blog.csdn.net/flower_drop](https://img.shields.io/badge/csdn-%40flower__drop-orange)


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


1. 由于接口文档编写耗时，而且需要持续维护，耗时耗力，使用此工具可以一键自动生成接口文档.
2. swagger-ui接口文档一键生成jmx文件供jmeter使用.


## 功能


1. 将swagger-ui文档转换为jmx文件


## Demo


```python
# -*- coding: utf-8 -*-

from swaggerjmx.convert import conversion
from swaggerjmx.settings import Settings as ST
#  swagger_url
ST.swagger_url = 'http://ip+端口/v2/api-docs'
#  report_path
ST.report_path = 'jmx'
# 开始转换
conversion()

```
