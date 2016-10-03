# coding:utf-8
from flask import render_template

from . import clothespress


@clothespress.route('/')
def index():
    return render_template('clothespress/index.html')
