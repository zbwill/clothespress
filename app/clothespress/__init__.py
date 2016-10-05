# coding:utf-8
from flask import Blueprint
from flask import url_for

clothespress = Blueprint('clothespress', __name__)

from . import views, errors

from ..models import Clothes, ClothesType

@clothespress.app_context_processor
def inject_row_menu():
    clothes_type_list = ClothesType.query.all()
    row_menu_list = []
    row_menu_list.append({'id': 'index', 'url': url_for('clothespress.index'), 'name': '首页'})
    for clothes_type in clothes_type_list:
        row_menu_list.append(
            {'id': 'clothes_type_{clothesTypeId}'.format(clothesTypeId=clothes_type.id),
             'url': url_for('clothespress.clothes_by_type', clothesTypeId=clothes_type.id),
             'name': clothes_type.typeName})
    row_menu_list.append({'id': 'clothes_type', 'url': url_for('clothespress.clothes_type_manage'), 'name': '衣服类型管理'})
    return {'row_menu_list': row_menu_list}
