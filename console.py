"""
在设计文件遍历和处理熟顺序时，先对配置文件进行处理，
遍历过程中或许仍要对它进行二次处理，但使用单一的
regexp匹配规则而不再对文件是否是配置文件做判断。
其中配置文件的指定，应支持输入一个文件夹或者一个文本文件

说明：在

"""
from project_killer import traverse_directory, filter_catalog
from config import *
from loglib.logger import Logger
from util.gettext_pipeline import *
from util.batch_translator import PoFileTranslator
log = Logger().get_logger()


def pipeline(language_to):
    tagging(output_file)
    xgettext('zh')
    interpreter = PoFileTranslator('zh', language_to)
    interpreter.batch_operator()
    msgfmt('zh')


if __name__ == '__main__':
    traverse_directory(PROJECT_ROOT)
    filter_catalog(output_file)
    pipeline('en')
