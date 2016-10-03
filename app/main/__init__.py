# coding:utf-8
from flask import Blueprint
from flask import url_for

main = Blueprint('main', __name__)


@main.app_context_processor
def inject_navbar():
    navbar_list = []
    navbar_list.append({'url': url_for('clothespress.index'), 'name': '衣橱'})
    return {'navbar_list': navbar_list}
