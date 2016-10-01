# coding:utf-8
from flask import Blueprint

clothespress = Blueprint('clothespress', __name__)

from . import views, errors
