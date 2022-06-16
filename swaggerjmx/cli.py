#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Lijiawei
@Date    :  2022/6/6 10:27 上午
@Desc    :  cli line.
"""
import argparse
import sys
from swaggerjmx import __description__
from swaggerjmx.convert import conversion


def main():
    """Parse command line options and run commands.
    """
    parser = argparse.ArgumentParser(description=__description__)

    parser.add_argument(
        '-i', '--input', help='The input swagger json file or swagger url.', required=True)
    parser.add_argument(
        '-o', '--output', help='The output jmx file path(default jmx). If it exists, old file will be overwrite.',
        default="jmx")

    args = parser.parse_args()

    from swaggerjmx.settings import Settings as ST
    if str(args.input).startswith("http"):
        ST.swagger_url = args.input
    elif str(args.input).endswith(".json"):
        ST.swagger_url_json_path = args.input
    else:
        parser.print_help()
        sys.exit(0)
    #  report_path
    ST.report_path = args.output
    conversion()
