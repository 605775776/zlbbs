# coding:utf8
# 2020/8/16 13:05
# author:dsw

from flask import Blueprint

bp = Blueprint('front', __name__)

@bp.route('/')
def index():
    return 'front index'
