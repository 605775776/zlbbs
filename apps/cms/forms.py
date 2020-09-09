# coding:utf8
# 2020/8/16 13:06
# author:dsw

from wtforms import Form, StringField, IntegerField, ValidationError
from wtforms.validators import Email, InputRequired, Length, EqualTo
from apps.forms import BaseForm
from utils import zlcache
from flask import g


class LoginForm(BaseForm):
    email = StringField(validators=[Email(message="请输入正确的邮箱格式"), InputRequired(message="邮箱不能为空")])
    password = StringField(validators=[Length(2, 20, message="请输入正确格式的密码")])
    remeber = IntegerField()


class ResetpwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(2, 20, message="请输入正确格式的旧密码")])
    newpwd = StringField(validators=[Length(2, 20, message="请输入正确格式的新密码")])
    newpwd2 =StringField(validators=[EqualTo("newpwd", message="两次输入的密码不一致")])


class ResetEmailForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确格式的邮箱')])
    captcha = StringField(validators=[Length(min=6, max=6, message="请输入正确长度的验证码")])

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_cache = zlcache.get(email)
        if not captcha_cache or captcha.lower() != captcha_cache.lower():
            raise ValidationError("邮箱验证码错误")

    def validate_email(self, field):
        email = field.data
        user = g.cms_user
        if user.email == email:
            raise ValidationError("逗我玩呢？")

