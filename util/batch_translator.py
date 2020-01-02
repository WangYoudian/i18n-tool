import os
import re
from .youdao_client import translate


class PoFileTranslator:
    """
    Po文件的翻译类，初始化时指定源语言和目标语言
    """
    def __init__(self, data_from="", data_to=""):
        self.data_from = data_from
        self.data_to = data_to
        self.file_input = 'resource/languages/{lang}/LC_MESSAGES/demo.po'.format(lang=data_from)
        self.content_pattern = re.compile('".*?"')

    def validator(self):
        """
        验证翻译的可行性，处理出错信息的类
        :return:
        """
        pass

    def content_extracter(self, string):
        matches = re.findall(self.content_pattern, string)
        for match in matches:
            return match

    def batch_operator(self):
        translate_flag = False
        text = ''
        translation = ''
        counter = 1000  # 防止过度请求API接口导致次数用完
        with open(self.file_input, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                # msgid行
                if line.startswith('msgid'):
                    # 提取出待翻译内容
                    query = self.content_extracter(line)
                    print(query)
                    if query != '""':
                        translate_flag = True
                        translation = translate(self.data_from, self.data_to, query)
                        translation = self.content_extracter(translation)
                else:
                    # msgstr行
                    # translation内容不为空(虽然每次利用后只是用flag表示'清空')，则写入下一行的msgstr
                    if translate_flag and line.startswith('msgstr'):
                        line = 'msgstr ' + translation + '\n'
                        translate_flag = False
                text += line
                counter -= 1
                if counter < 0:
                    break
        os.chdir('/'.join(self.file_input.split('/')[:-1]))
        with open('demo.po', 'w', encoding='gbk') as f:
            f.write(text)


if __name__ == '__main__':
    po = PoFileTranslator('zh', 'en')
    po.batch_operator()
