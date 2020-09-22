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
    g,
    abort)
from .forms import SignupForm, SigninForm, AddPostForm, AddCommentForm
from utils import restful
from .models import FrontUser
from ..models import BannerModel, BoardModel, PostModel, CommentModel
from exts import db
from utils import safeutils
from .decorators import login_required
from flask_paginate import Pagination, get_page_parameter
import config


bp = Blueprint('front', __name__)

@bp.route('/')
def index():
    board_id = request.args.get('bd', type=int, default=None)
    page = request.args.get(get_page_parameter(), type=int, default=1)

    banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(4)
    boards = BoardModel.query.all()
    # posts = PostModel.query.all()
    start = (page-1)*config.PER_PAGE
    end = start +config.PER_PAGE
    post = None
    total = 0
    if board_id:
        query_obj = PostModel.query.filter_by(board_id=board_id)
        posts = query_obj.slice(start, end)
        total = query_obj.count()
        # posts = PostModel.query.filter_by(board_id=board_id).slice(start, end)
        # total = PostModel.query.filter_by(board_id=board_id).count()
    else:
        posts = PostModel.query.slice(start, end)
        total = PostModel.query.count()
    pagination = Pagination(bs_version=3, page=page, total=total, outer_window=0, inner_window=2)
    context = {"banners": banners,
               "boards": boards,
               "posts": posts,
               "pagination": pagination,
               "current_board": board_id}
    return render_template('front/front_index.html', **context)

@bp.route('/p/<post_id>')
def post_detail(post_id):
    post = PostModel.query.get(post_id)
    # comments = CommentModel.query.all()
    if not post:
        abort(404)
    return render_template('front/front_pdetail.html', post=post)


@bp.route('/acomment/', methods=['POST'])
@login_required
def add_comment():
    form = AddCommentForm(request.form)
    if form.validate():
        content = form.content.data
        post_id = form.post_id.data
        post = PostModel.query.get(post_id)
        if post:
            comment = CommentModel(content=content)
            comment.post = post
            comment.author = g.front_user
            db.session.add(comment)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error("没有这篇帖子")
    else:
        return restful.params_error(form.get_error())




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
