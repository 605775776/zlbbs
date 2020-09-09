# encoding:utf-8
# 2020/8/16 21:55
# author:dsw

from flask import session, redirect, url_for
from functools import wraps
import config

def login_required(func):

    @wraps(func)
    def inner(*args, **kwargs):
        if config.CMS_USER_ID in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('cms.login'))

    return inner
