# coding:utf-8
import gettext

def print_en():
    _ = gettext.gettext
    print('\nEnglish:')
    print(_('You are a sweet girl!'))
    print(_('My name is {name}').format(name='orangleliu'))

def print_zh():
    t = gettext.translation('demo', 'locale', languages=["zh_CN"])
    _ = t.gettext
    print('\n中文:')
    print(_('You are a sweet girl!'))
    print(_('My name is {name}').format(name='orangleliu'))

if __name__ == '__main__':
    print_en()
    print_zh()