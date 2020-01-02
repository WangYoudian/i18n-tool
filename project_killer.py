import os
import re
import time

from config import *
from resource.parser import PythonRule
from loglib.logger import Logger

log = Logger().get_logger()

PROJECT_ROOT = 'E:/corepro/corepro-b-cai-front-service'
CONFIGURATION = ['common_lib.py']
search_type = ['.py']
rule_of_python = PythonRule()


def traverse_directory(directory):
    for root, dirs, files in os.walk(directory):
        if files:
            for file in files:
                if os.path.splitext(file)[1] in search_type:
                    filename = os.path.join(root, file)
                    if file in CONFIGURATION:
                        process_config(filename)
                    process(filename)

        if dirs:
            for sub_directory in dirs:
                full_sub_dir = os.path.join(root, sub_directory)
                traverse_directory(full_sub_dir)


def process(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        stream_in = remove_comment(f.read())
    rule_of_python.regexp(stream_in)


def process_config(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        stream_in = remove_comment(f.read())
        # print(stream_in)
    rule_of_python.rule_configuration(stream_in, ':')


def remove_comment(code):
    """
    # TODO:前提是match在文件中具有唯一性
    :param code:
    :return:
    """
    maps = re.findall(re.compile('#.*?\n'), code)
    for match in maps:
        code = code.replace(match, "\n")
    maps = re.findall(re.compile('""".*?"""', re.DOTALL), code)
    for match in maps:
        code = code.replace(match, "\n")
        # print(match)
        # time.sleep(1)
    return code


def filter_catalog(file):
    """
    修改内容在这个函数中实现
    :param file: 输入为包含英文句子还有各种奇葩Exception中内容
    :return:
    """
    zh_pattern = re.compile(r'[\u4e00-\u9fa5]')
    text = ''
    # 文档去重
    with open('demo.txt', 'r', encoding='gbk') as f:
        ts = f.readlines()
        sentences = set(ts)
    # print(''.join(sentences))
    # 中间临时文件，每次都会被覆盖
    with open('demo_filter.txt', 'w', encoding='gbk') as f:
        f.write(''.join(sentences))
    # 去除不含中文的句子(纯英文)
    with open('demo_filter.txt', 'r', encoding='gbk') as f:
        for line in f.readlines():
            result = re.findall(zh_pattern, line)
            if result:
                text += line
            else:
                continue
    print(text)
    with open('demo.txt', 'w', encoding='gbk') as f:
        f.write(text)


def filter_catalog_deprecated(file):
    """
    这个函数一开始设计的不是很好，因为上游的正则发现规则写的不是很好，在后面的修改中重写
    :param file:
    :return:
    """
    text = ''
    zh_character = re.compile(r"[\u4e00-\u9fa5]+")
    # Done 解决形如"输入的操作系统[%s]不存在"%dataObj["OS"]后的%问题 -> 输入的操作系统不存在  利用用户上下文
    # TODO: 在上面的基础上去除[]及其中的内容
    # bracket = re.compile('[.*?]')
    with open(file, 'r', encoding='gbk') as f:
        log.info("Length before filtering the catalog text is as follows...")
        log.info(len(f.readlines()))
        time.sleep(3)
        sentences = set(f.readlines())
        # for line in f.readlines():
        #     if not re.findall(zh_character, line):
        #         pass
            # else:
            #     print(line)
            #     # 发现使用 % 动态赋值的line
            #     if line.find('"%') != -1 or line.find('" %') != -1:
            #         # 不做处理 也不加入
            #         # continue
            #         # 处理一
            #         # print(line)
            #         # # 实际上在parser过程中已经将' '去除
            #         # fragments = line.replace('\n', '').split('"%')
            #         # line = fragments[0] + '".format(' + fragments[1] + ')'
            #         # print(line.strip())
            #         # time.sleep(1)
            #         # 处理二
            #         print(line.strip())
            #         line = line.replace('为[%s]', '').split('"%')[0] + '"\n'
            #         log.info(line.strip() + '\n')
            #     # if line.find('"') == -1:
            #     #     # 有些定义出现了没有双引号的异常 这些在后续改动正则时做了优化
            #     #     #
            #     #     line = '"' + line + '"'
            #     text += line
    log.info('text is ' + text)
    with open(file, 'w', encoding='utf-8') as f:
        sentences = set(text.split('\n'))
        print('\n'.join(sentences))
        f.write('\n'.join(sentences))


if __name__ == '__main__':
    traverse_directory(PROJECT_ROOT)
    filter_catalog(output_file)
