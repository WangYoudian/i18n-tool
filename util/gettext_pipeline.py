# coding: utf-8
"""
第二阶段：
gettext流水线：
（1）加'_'标记，并生成demo.py
#（2）xgettext -o [languages/zh/LC_CLASSES/]demo.po demo.py --from-code utf-8
并修改CHARSET为UTF-8
*（3）读po文件，请求有道翻译API，自动填充msgstr字段。
（3-1）支持对生成的msgstr修改，并自动进行（4）操作
（4）msgfmt -o demo.mo demo.po
"""
import os
from loglib.logger import Logger

log = Logger().get_logger()


def tagging(txt_catalog_file):
    with open('demo.py', 'w', encoding='utf-8') as catalog:
        # 调用gettext.gettext对demo.py中的代码做标记
        catalog.write("from gettext import gettext as _" + '\n\n')
        with open(txt_catalog_file, 'r', encoding='gbk') as file:
            for item in file.readlines():
                if item == '\n':
                    # 空行
                    continue
                catalog.write('_("' + item.strip() + '")\n')
        log.info("Write into demo.py...")


def xgettext(lang_version):
    """
    生成msgid从demo.py中提取，以及msgstr为空的po文件
    这个po文件是可以多个语言共用的，但是为了区别起见，还是对每种语言做一个区分
    执行xgettext工具，格式为：xgettext -o [languages/zh/LC_CLASSES/]demo.po demo.py --from-code utf-8
    其中zh为lang_version变量提供
    做完这步处理前记得将CHARSET replace成 UTF-8
    :param lang_version:
    :return:
    """
    # TODO: 当人工/机器自动翻译后，每个po文本语言类型就是base语言版本+翻译指定语言版本，这个版本控制参数还可以在哪里指定？
    cmd = "xgettext -o resource/languages/{lang}/LC_MESSAGES/demo.po demo.py --from-code utf-8".format(lang=lang_version)
    try:
        log.info("若提示No such file or directory，请手动创建对应的文件夹")
        os.system(cmd)
        log.warning(cmd)
    except OSError:
        # TODO: 这里定义的类型咱也不知道，但就是不想用Exception
        log.error(str(OSError))
    except Exception as err:
        log.error(str(err))


def msgfmt(lang_version):
    """
    外部操作为：进入工作文件夹，执行msgfmt命令，回到原来的目录
    这里是为处理涉及三种及以上语言的兼容
    :return:
    """
    # po_path = "resource/languages/{lang}/LC_MESSAGES/demo.po".format(lang=lang_version)
    # mo_path = "resource/languages/{lang}/LC_MESSAGES/demo.mo".format(lang=lang_version)
    po_path = "resource/languages/{lang}/LC_MESSAGES/demo.po".format(lang=lang_version)
    mo_path = "resource/languages/{lang}/LC_MESSAGES/demo.mo".format(lang=lang_version)
    cmd = 'msgfmt -o {0} {1}'.format(mo_path, po_path)
    log.info("如果提示No such file or directory，多半是相对路径需要去除../")
    try:
        os.system(cmd)
        log.warning(cmd)
    except OSError:
        # TODO: 这里定义的类型咱也不知道，但就是不想用Exception
        log.error(str(OSError))

if __name__ == '__main__':
    msgfmt('zh')