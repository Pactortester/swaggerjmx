# -*- coding:utf-8 -*-
import os
import site

BASE_DIR = os.getcwd()
USER_PTH = os.path.join(site.getsitepackages()[-1], 'requirements.pth')


def main():
    try:
        os.remove(USER_PTH)
    except FileNotFoundError:
        pass
    with open(USER_PTH, 'w') as f:
        f.write(BASE_DIR)
        print("生成文件成功！")
        print("文件位置：%s" % USER_PTH)
    with open(USER_PTH) as f:
        print("文件内容：", f.read())


if __name__ == '__main__':
    main()