# coding:utf-8
from . import clothespress


@clothespress.route('/')
def demo():
    return 'hello demo'
