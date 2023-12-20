#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re
import os
import opencc
import googletrans
import concurrent.futures
import threading

# 创建一个全局的线程锁
lock = threading.Lock()

def translate_file(file_path):
    # 定义正则表达式，匹配中文字符
    pattern = re.compile('[\u4e00-\u9fa5]+')
    # 定义三个字典，存放英文、简体中文和繁体中文的翻译结果
    dict_en = {}
    dict_zh = {}
    dict_tw = {}
    # 创建一个翻译器对象
    translator = googletrans.Translator()
    # 创建一个简体中文到繁体中文的转换器
    converter = opencc.OpenCC('s2t.json')

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
            key = tag  # 使用原始的中文文本作为键
            value_en = translated_tag.text
            value_zh = tag
            value_tw = converter.convert(tag)  # 将简体中文文本转换为繁体中文
            if page not in dict_en:
                dict_en[page] = {}
            if page not in dict_zh:
                dict_zh[page] = {}
            if page not in dict_tw:
                dict_tw[page] = {}
            dict_en[page][key] = value_en
            dict_zh[page][key] = value_zh
            dict_tw[page][key] = value_tw

    return dict_en, dict_zh, dict_tw

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
    result_tw = {}
    for dict_en, dict_zh, dict_tw in dicts:
        result_en.update(dict_en)
        result_zh.update(dict_zh)
        result_tw.update(dict_tw)

    # 将结果写入zh_CN.js文件
    zh_CN_path = os.path.join(project_path, 'i18n/zh_CN.js')
    with open(zh_CN_path, 'w', encoding='utf-8') as f:
        f.write('// zh_CN.js\n')
        f.write('const languageMap = {\n')
        for page, values in result_zh.items():
            f.write(f'  // {page}",\n')
            for key, value in values.items():
                f.write(f'  "{key}": "{value}",\n')
        f.write('}\n')
        f.write('\nmodule.exports = {\n')
        f.write('  languageMap: languageMap\n')
        f.write('}\n')
        f.write('\n')

    # 将结果写入en.js文件
    en_path = os.path.join(project_path, 'i18n/en.js')
    with open(en_path, 'w', encoding='utf-8') as f:
        f.write('// en.js\n')
        f.write('const languageMap = {\n')
        for page, values in result_en.items():
            f.write(f'  // {page}",\n')
            for key, value in values.items():
                f.write(f'  "{key}": "{value}",\n')
        f.write('}\n')
        f.write('\nmodule.exports = {\n')
        f.write('  languageMap: languageMap\n')
        f.write('}\n')
        f.write('\n')

    # 将结果写入zh_TW.js文件
    zh_TW_path = os.path.join(project_path, 'i18n/zh_TW.js')
    with open(zh_TW_path, 'w', encoding='utf-8') as f:
        f.write('// zh_TW.js\n')
        f.write('const languageMap = {\n')
        for page, values in result_tw.items():
            f.write(f'  // {page}",\n')
            for key, value in values.items():
                f.write(f'  "{key}": "{value}",\n')
        f.write('}\n')
        f.write('\nmodule.exports = {\n')
        f.write('  languageMap: languageMap\n')
        f.write('}\n')
        f.write('\n')

if __name__ == '__main__':
    project_path = 'D:\\IdeaProjects\\dts-shop\\wx-mini-program'
    translationProject(project_path)
