##!/usr/bin/python3
# -*- coding: utf-8 -*-
import re
import os
import json
import googletrans
import concurrent.futures
import threading

# 创建一个全局的线程锁
lock = threading.Lock()

def translate_file(file_path):
    # 定义正则表达式，匹配中文字符
    pattern = re.compile('[\u4e00-\u9fa5]+')
    # 定义两个字典，存放英文和中文的翻译结果
    dict_en = {}
    dict_zh = {}
    # 创建一个翻译器对象
    translator = googletrans.Translator()

    path = file_path
    # 获取文件名，去掉后缀
    page = os.path.basename(file_path).split('.')[0]
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        # 使用正则表达式，找出文件内容中的所有中文标签
        tags = pattern.findall(content)
        # 使用线程锁保护翻译过程
        with lock:
            # 一次性翻译所有的标签
            translated_tags = translator.translate(tags, src='zh-cn', dest='en')
        for tag, translated_tag in zip(tags, translated_tags):
            key = translated_tag.text.lower().replace(" ", "_")
            value_en = translated_tag.text
            value_zh = tag
            if page not in dict_en:
                dict_en[page] = {}
            if page not in dict_zh:
                dict_zh[page] = {}
            dict_en[page][key] = value_en
            dict_zh[page][key] = value_zh

    return dict_en, dict_zh

def translationProject(project_path):
    # 获取pages文件夹的路径
    pages_path = os.path.join(project_path, 'pages')
    # 获取所有.wxml文件的路径
    files = [os.path.join(root, file) for root, dirs, files in os.walk(pages_path) for file in files if file.endswith('.wxml')]

    # 使用线程池并发处理所有文件
    with concurrent.futures.ThreadPoolExecutor() as executor:
        dicts = list(executor.map(translate_file, files))

    result_en = {}
    result_zh = {}
    for dict_en, dict_zh in dicts:
        result_en.update(dict_en)
        result_zh.update(dict_zh)

    # 将结果写入en.js文件
    en_path = os.path.join(project_path, 'en.js')
    with open(en_path, 'w', encoding='utf-8') as f:
        f.write('// en.js\n')
        f.write('module.exports = \n')
        json.dump(result_en, f, ensure_ascii=False, indent=4)
        f.write('\n')

    # 将结果写入zh.js文件
    zh_path = os.path.join(project_path, 'zh.js')
    with open(zh_path, 'w', encoding='utf-8') as f:
        f.write('// zh.js\n')
        f.write('module.exports = \n')
        json.dump(result_zh, f, ensure_ascii=False, indent=4)
        f.write('\n')

    f.close()

if __name__ == '__main__':
    project_path = 'D:\IdeaProjects\dts-shop\wx-mini-program'
    translationProject(project_path)
