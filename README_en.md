# swaggerjmx
[![Build Status](https://travis-ci.com/Pactortester/swaggerjmx.svg?branch=master)](https://travis-ci.com/Pactortester/swaggerjmx) ![PyPI](https://img.shields.io/pypi/v/swaggerjmx) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/swaggerjmx) ![GitHub top language](https://img.shields.io/github/languages/top/Pactortester/swaggerjmx) [![Downloads](https://static.pepy.tech/personalized-badge/swaggerjmx?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=downloads/total)](https://pepy.tech/project/swaggerjmx) ![GitHub stars](https://img.shields.io/github/stars/Pactortester/swaggerjmx?style=social) ![https://blog.csdn.net/flower_drop](https://img.shields.io/badge/csdn-%40flower__drop-orange)

**[Chinese Document](./README.md)**

## Logo

![logo](https://files.mdnice.com/user/17535/09daca64-e43e-44fa-af31-d785a75a9194.png)


## Install

```shell
pip install -U swaggerjmx
```

##  Warehouse Address：


- github：https://github.com/Pactortester/swaggerjmx.git
- pypi：https://pypi.org/project/swaggerjmx


## Community address


- testerhome：https://testerhome.com/opensource_projects/swaggerjmx


## Applicable scene

1. Since the writing of interface test scripts is time-consuming and requires continuous maintenance, which is time-consuming and labor-intensive, you can use this tool to generate interface test scripts with one click.
2. The swagger-ui interface document generates jmx files with one click for use by jmeter.
3. The yapi interface document generates a jmx file with one click for use by jmeter.

## Features

1. Convert swagger-ui documents to jmx file.
2. Convert the yapi document to jmx file.

## Code way
### Demo_1
- Can be accessed directly swagger_url (http://ip:port/v2/api-doc) Don’t need to log in, use Demo_1 to convert.

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


### Demo_2
- If you need to log in to access, you can copy the json information on the swagger_url page, save the json file, and use Demo_2 to convert.

```python
# -*- coding: utf-8 -*-

from swaggerjmx.convert import conversion
from swaggerjmx.settings import Settings as ST
#  swagger_url_json_path 
ST.swagger_url_json_path = 'tests/data/swagger.json'
#  report_path
ST.report_path = 'jmx'
# Start conversion
conversion()

```

## Command line mode
### Preset parameters
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
### Usage
```shell
swaggerjmx -i <path_to_swagger_json_or_swagger_url> -o <path_to_output_jmx>
```
## Screenshot：

1. Pass in the swagger-ui address in the red box.

![image](https://user-images.githubusercontent.com/29191106/88256748-a58d3900-ccee-11ea-8960-b16ed18c34c6.png)

2. Generated jmx file.

![image](https://user-images.githubusercontent.com/29191106/88256097-de2c1300-ccec-11ea-80cb-4a2ed6e8c4e0.png)

3. display in jmeter.

![image](https://user-images.githubusercontent.com/29191106/88256407-d91b9380-cced-11ea-910b-cafaec9ae158.png)

## Trend

[![Stargazers over time](https://starchart.cc/Pactortester/swaggerjmx.svg)](https://starchart.cc/Pactortester/swaggerjmx)

## Contributors

<a href="https://github.com/Pactortester/swaggerjmx/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Pactortester/swaggerjmx" />
</a>

## Contribute and develop

```shell
git clone git@github.com:Pactortester/swaggerjmx.git
cd swaggerjmx
pip install -e .
```
## 

The above is an introduction to the basic usage of swaggerjmx.

If you find a bug, or if you have any suggestions for swaggerjmx, welcome [swaggerjmx Issues](https://github.com/Pactortester/swaggerjmx/issues) published, thank you very much for your support. Your feedback and suggestions are very valuable, and I hope your participation can help swaggerjmx do better.
