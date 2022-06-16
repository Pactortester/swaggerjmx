# swaggerjmx

[![codecov](https://codecov.io/gh/Pactortester/swaggerjmx/branch/master/graph/badge.svg)](https://codecov.io/gh/Pactortester/swaggerjmx) ![PyPI](https://img.shields.io/pypi/v/swaggerjmx) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/swaggerjmx) ![GitHub top language](https://img.shields.io/github/languages/top/Pactortester/swaggerjmx) [![Downloads](https://static.pepy.tech/personalized-badge/swaggerjmx?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=downloads/total)](https://pepy.tech/project/swaggerjmx) ![GitHub stars](https://img.shields.io/github/stars/Pactortester/swaggerjmx?style=social) ![https://blog.csdn.net/flower_drop](https://img.shields.io/badge/csdn-%40flower__drop-orange)

**[English Document](./README_en.md)**
## Logo

![logo](https://files.mdnice.com/user/17535/09daca64-e43e-44fa-af31-d785a75a9194.png)

## 安装

```shell
pip install -U swaggerjmx
```

##  仓库地址


- github：https://github.com/Pactortester/swaggerjmx.git
- pypi：https://pypi.org/project/swaggerjmx


## 社区地址


- testerhome：https://testerhome.com/opensource_projects/swaggerjmx


## 适用场景


1. 由于接口测试脚本编写耗时，而且需要持续维护，耗时耗力，使用此工具可以一键生成接口测试脚本。
2. swagger-ui接口文档一键生成jmx文件供jmeter使用。
3. yapi接口文档一键生成jmx文件供jmeter使用。


## 功能


1. 将swagger-ui文档转换为jmx文件。
2. 将yapi文档转换为jmx文件。

## 代码方式
### Demo_1
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


### Demo_2
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

## 命令行方式
### 预置参数
```shell
(venv) lijiawei@bogon swaggerjmx % swaggerjmx -h
usage: swaggerjmx [-h] -i INPUT [-o OUTPUT]

Swagger or YApi convert jmx tool! Created: Lijiawei. Version 1.1.0

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        The input swagger json file or swagger url.
  -o OUTPUT, --output OUTPUT
                        The output jmx file path(default jmx). If it exists, new endpoints will be overwrite.
```
### 使用方式
```shell
swaggerjmx -i <path_to_swagger_json_or_swagger_url> -o <path_to_output_jmx>
```
### swagger json example
```shell
swaggerjmx -i tests/data/swagger.json -o jmx
```
### swagger url example
```shell
swaggerjmx -i https://ip:port/v2/api-docs -o jmx
```
## 截图：

1. 传入红框中的swagger-ui 地址

![image](https://user-images.githubusercontent.com/29191106/88256748-a58d3900-ccee-11ea-8960-b16ed18c34c6.png)

2. 生成的jmx文件

![image](https://user-images.githubusercontent.com/29191106/88256097-de2c1300-ccec-11ea-80cb-4a2ed6e8c4e0.png)

3. jmeter中显示

![image](https://user-images.githubusercontent.com/29191106/88256407-d91b9380-cced-11ea-910b-cafaec9ae158.png)

## 趋势图

[![Stargazers over time](https://starchart.cc/Pactortester/swaggerjmx.svg)](https://starchart.cc/Pactortester/swaggerjmx)

## Contributors

<a href="https://github.com/Pactortester/swaggerjmx/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Pactortester/swaggerjmx" />
</a>

## 贡献
```shell
git clone git@github.com:Pactortester/swaggerjmx.git
cd swaggerjmx
pip install -e .
```

## 

以上便是 swaggerjmx 的基本用法介绍。

如果您有发现错误，或者您对 swaggerjmx 有任何建议，欢迎到 [swaggerjmx Issues](https://github.com/Pactortester/swaggerjmx/issues) 发表，非常感谢您的支持。您的反馈和建议非常宝贵，希望您的参与能帮助 swaggerjmx 做得更好。
