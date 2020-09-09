# coding:utf-8
# 2020/8/20 17:15
# Author:dsw

from wtforms import Form

class BaseForm(Form):
    def get_error(self):
        message = self.errors.popitem()[1][0]
        return message