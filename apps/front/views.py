# coding:utf8
# 2020/8/16 13:05
# author:dsw

from flask import (
    Blueprint,
    views,
    render_template,
    session,
    request,
    url_for,
    g)
from .forms import SignupForm, SigninForm, AddPostForm
from utils import restful
from .models import FrontUser
from ..models import BannerModel, BoardModel, PostModel
from exts import db
from utils import safeutils
from .decorators import login_required
import config


bp = Blueprint('front', __name__)

@bp.route('/')
def index():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(4)
    boards = BoardModel.query.all()
    posts = PostModel.query.all()
    context = {"banners": banners,
               "boards": boards,
               "posts": posts}
    return render_template('front/front_index.html', **context)


@bp.route('/apost/', methods=['GET', 'POST'])
@login_required
def apost():
    if request.method == 'GET':
        boards = BoardModel.query.all()
        return render_template('front/front_apost.html',boards=boards)

    else:
        form = AddPostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            board = BoardModel.query.get(board_id)
            if not board:
                return restful.params_error(message="板块id不存在")

            post = PostModel(title=title, content=content)
            post.board = board
            post.author = g.front_user
            db.session.add(post)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message=form.get_error())










class SignupView(views.MethodView):
    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and safeutils.is_safe_url(return_to):
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
bp.add_url_rule('/signin/', view_func=SigninView.as_view('signin'))
