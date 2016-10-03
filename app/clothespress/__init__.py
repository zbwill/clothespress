# coding:utf-8
from flask import Blueprint
from flask import url_for

clothespress = Blueprint('clothespress', __name__)

from . import views, errors


@clothespress.app_context_processor
def inject_row_menu():
    row_menu_list = []
    row_menu_list.append({'id': 'index', 'url': url_for('clothespress.index'), 'name': '首页'})
    return {'row_menu_list': row_menu_list}
