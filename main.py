##!/usr/bin/python3
# -*- coding: utf-8 -*-


# https://blog.csdn.net/weixin_47124112/article/details/129683864


import os
import json
import shutil
from glob import glob


def initProject(project_path):

    # 任务1: 拷贝switchLanguage文件夹下面所有文件至项目下面的components目录下面 如果不存在则创建components
    src_dir = 'switchLanguage'
    dst_dir = os.path.join(project_path, 'components', 'switchLanguage')
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    for file_name in os.listdir(src_dir):
        src_file = os.path.join(src_dir, file_name)
        dst_file = os.path.join(dst_dir, file_name)
        if os.path.isfile(src_file):
            shutil.copy(src_file, dst_file)

    util_dir = os.path.join(project_path, 'utils')
    if not os.path.exists(util_dir):
        os.makedirs(util_dir)

    # 任务2: 拷贝language.js 拷贝项目下目录utils 下
    shutil.copy('language.js', util_dir)

    # 任务3: 读取app.json目录下面 内容读取是否存在usingComponents至
    # 如果存在 则在下面添加内容 "switchLanguage": "./components/switchLanguage/index"
    # 如果存在则添加 "usingComponents": {"switchLanguage": "./components/switchLanguage/index"}
    with open(os.path.join(project_path, 'app.json'), 'r+') as f:
        data = json.load(f)
        if 'usingComponents' in data:
            data['usingComponents']['switchLanguage'] = "./components/switchLanguage/index"
        else:
            data['usingComponents'] = {"switchLanguage": "./components/switchLanguage/index"}
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

    # 任务4: 读取所有pages文件夹下的.js 文件内容 第一行插入内容 const base = require('../../utils/language.js') const _ = base._
    for file_name in glob(os.path.join(project_path, 'pages/**/*.js'), recursive=True):
        with open(file_name, 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            f.write("const base = require('../../utils/language.js')\nconst _ = base._\n" + content)


if __name__ == '__main__':
    # 定义项目路径
    project_path = 'D:\\IdeaProjects\\dts-shop\\wx-mini-program'
    initProject(project_path)
