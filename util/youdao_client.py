import sys
import uuid
from pprint import pprint

import requests
import hashlib
import time
import json
from imp import reload
import time
from loglib.logger import Logger

log = Logger().get_logger()
reload(sys)

YOUDAO_URL = 'https://openapi.youdao.com/api'
APP_KEY = '79c2a49e113af228'
APP_SECRET = 'nUzczKXcv8C6TJr9Wlo089hyZ2MKB2a8'


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    """
    待翻译内容不得长于20个字符
    :param q:
    :return:
    """
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)


def translate(data_from, data_to, query):
    """
    请求有道词典API，翻译query
    :param data_from: 待翻译语言版本
    :param data_to: 目标版本
    :param query: 待翻译内容
    :return: translation，即翻译的内容
    """
    data = {}

    # 暂时只做中译英的支持 可以用一个map把项目里的标准统一成API接口的标准
    # data['from'] = data_from
    if data_from == 'zh':
        data['from'] = 'zh-CHS'
    else:
        data['from'] = 'zh-CHS'
    # data['to'] = data_to
    if data_to == 'en':
        data['to'] = 'EN'
    else:
        data['to'] = 'EN'
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(query) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['q'] = query
    data['salt'] = salt
    data['sign'] = sign

    response = do_request(data)
    # cutentType = response.headers['Content-Type']
    # print(response.content)  # a byte-like string   <class 'bytes'>
    # pprint(json.dumps(str(response.content.decode('utf-8'))))
    translation = json.loads(str(response.content.decode('utf-8')))['translation']
    log.info(query)
    log.info(translation)  # <class 'list'>
    return translation[0]


def connect_raw():
    q = "待输入的文字"

    data = {}
    data['from'] = 'zh-CHS'
    data['to'] = 'EN'
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['q'] = q
    data['salt'] = salt
    data['sign'] = sign

    response = do_request(data)
    contentType = response.headers['Content-Type']
    if contentType == "audio/mp3":
        millis = int(round(time.time() * 1000))
        filePath = "合成的音频存储路径" + str(millis) + ".mp3"
        fo = open(filePath, 'wb')
        fo.write(response.content)
        fo.close()
    else:
        print(response.content)
        # class 'bytes'
        res = str(response.content.decode('utf-8'))  # .replace("'", '"')
        # print(res)
        data = json.loads(res)
        s = json.dumps(data, indent=4, sort_keys=True)
        print(s)
        # print(type(s))
        # <class 'str'>
        # print(type(data))
        # <class 'dict'>
        query = data["query"]  # unicode
        query = query.encode('utf-8').decode(encoding="utf-8")
        print(query, end='')
        print(":")
        print(data["translation"])


if __name__ == '__main__':
    # connect_raw()
    # translate('zh-CHS', 'EN', '合成的音频存储路径')
    translate('zh-CHS', 'EN', "return{'tree_name':'tree-1''full_name':'深圳-龙华-CCC'}这种格式或者抛出异常")
