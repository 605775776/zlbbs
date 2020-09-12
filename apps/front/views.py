# coding:utf8
# 2020/8/16 13:05
# author:dsw

from flask import (
    Blueprint,
    views,
    render_template,
    session,
    request,
    url_for)
from .forms import SignupForm, SigninForm
from utils import restful
from .models import FrontUser
from exts import db
from utils import safeutils
import config


bp = Blueprint('front', __name__)

@bp.route('/')
def index():
    return 'front index'


class SignupView(views.MethodView):
    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and safeutils.is_sage_url(return_to):
            return render_template('front/front_signup.html', return_to=return_to)
        else:
            return render_template('front/front_signup.html')

    def post(self):
        form = SignupForm(request.form)
        if form.validate():
            username = form.username.data
            password = form.password1.data
            user = FrontUser(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return restful.success()

        else:
            print(form.get_error())
            return restful.params_error(message=form.get_error())

class SigninView(views.MethodView):
    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and return_to != url_for('front.signup') and safeutils.is_safe_url(return_to):
            return render_template('front/front_signin.html', return_to=return_to)
        else:
            return render_template('front/front_signin.html')

    def post(self):
        form = SigninForm(request.form)
        if form.validate():
            username = form.username.data
            password = form.password.data
            remeber = form.remeber.data
            user = FrontUser.query.filter_by(username=username).first()
            if user and user.check_password(password):
                session[config.Front_USER_ID] = user.id
                if remeber:
                    session.permanent = True
                return restful.success()
            else:
                return restful.params_error(message="用户名或密码错误")
        else:
            return  restful.params_error(message=form.get_error())



bp.add_url_rule('/signup/', view_func=SignupView.as_view('signup'))
bp.add_url_rule('/signin/', view_func=SignupView.as_view('signin'))
