# coding:utf-8
# 2020/9/17 13:46
# Author:dsw

from .views import bp
import config
from flask import session, g, render_template
from .models import FrontUser
@bp.before_request
def my_before_request():

    if config.Front_USER_ID in session:
        user_id = session.get(config.Front_USER_ID)
        user = FrontUser.query.get(user_id)
        if user:
            g.front_user = user


@bp.errorhandler
def page_not_found():
    return render_template('front/front_404.html'), 404

