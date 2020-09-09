# coding:utf8
# 2020/8/16 13:05
# author:dsw

from flask import Blueprint

bp =Blueprint('common', __name__, url_prefix='/common')

@bp.route('/')
def index():
    return 'common index'
