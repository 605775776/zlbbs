# coding:utf8
# 2020/8/16 13:04
# author:dsw


from flask import (
    Blueprint,
    render_template,
    views,
    request,
    session,
    redirect,
    url_for,
    g,
    jsonify)
from .forms import (
    LoginForm,
    ResetpwdForm,
    ResetEmailForm,
    AddBannerForm,
    UpdateBannerForm,
    AddBoardForm,
    UpdateBoardForm)
from .models import CMSUser, CMSPermission
from ..models import BannerModel, BoardModel, PostModel, HighlightPostModel
from .decorators import login_required, permission_required
import config
from exts import db, mail
from utils import restful, zlcache
from flask_mail import Message
from tasks import send_mail

import string
import random

bp = Blueprint('cms', __name__, url_prefix='/cms')


@bp.route('/')
@login_required
def index():
    # g.cms_user
    return render_template('cms/cms_index.html')


@bp.route('/posts/')
@login_required
@permission_required(CMSPermission.POSTER)
def posts():
    # context = {
    #     'posts': PostModel.query.all()
    # }
    # return render_template('cms/cms_posts.html', **context)
    post_list = PostModel.query.all()
    return render_template('cms/cms_posts.html', posts=post_list)

@bp.route('/hpost/', methods=['POST'])
@login_required
@permission_required(CMSPermission.POSTER)
def hpost():
    post_id = request.form.get('post_id')
    if not post_id:
        return restful.params_error("请传入帖子id")

    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error("没有这个帖子")

    highlight = HighlightPostModel()
    highlight.post = post
    db.session.add(highlight)
    db.session.commit()
    return restful.success()

@bp.route('/uhpost/', methods=['POST'])
@login_required
@permission_required(CMSPermission.POSTER)
def uhpost():
    post_id = request.form.get('post_id')
    if not post_id:
        return restful.params_error("请传入帖子id")

    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error("没有这个帖子")
    highlight = PostModel.query.filter_by(post_id=post_id).first()
    db.session.delete(highlight)
    db.session.commit()
    return restful.success()

@bp.route('/comments/')
@login_required
@permission_required(CMSPermission.COMMENTER)
def comments():
    return render_template('cms/cms_comments.html')

@bp.route('/boards/')
@login_required
@permission_required(CMSPermission.BOARDER)
def boards():
    board_models = BoardModel.query.all()
    context = {
        'boards': board_models
    }
    return render_template('cms/cms_boards.html', **context)

@bp.route('/aboard/', methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def aboard():
    form = AddBoardForm(request.form)
    if form.validate():
        name = form.name.data
        board = BoardModel(name=name)
        db.session.add(board)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())

@bp.route('/uboard/', methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def uboard():
    form = UpdateBoardForm(request.form)

    if form.validate():
        board_id = form.board_id.data
        name = form.name.data
        board = BoardModel.query.get(board_id)
        if board:
            board.name = name
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message="没有这个板块")
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/dboard/', methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def dboard():
    board_id = request.form.get('board_id')
    if not board_id:
        return restful.params_error(message="请输入板块id")

    board = BoardModel.query.get(board_id)
    if not board:
        return restful.params_error(message="该板块不存在")

    db.session.delete(board)
    db.session.commit()
    return restful.success()




@bp.route('/fusers/')
@login_required
@permission_required(CMSPermission.FRONTUSER)
def fusers():
    return render_template('cms/cms_fusers.html')

@bp.route('/cusers/')
@login_required
@permission_required(CMSPermission.CMSUSER)
def cusers():
    return render_template('cms/cms_cusers.html')

@bp.route('/croles/')
@login_required
@permission_required(CMSPermission.ALL_PERMISSION)
def croles():
    return render_template('cms/cms_croles.html')

@bp.route('/banners/')
@login_required
def banners():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).all()
    return render_template('cms/cms_banners.html', banners=banners)

@bp.route('/abanner/', methods=['POST'])
@login_required
def abanner():
    form = AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel(name=name, image_url=image_url, link_url=link_url, priority=priority)
        db.session.add(banner)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())

@bp.route('/ubanner/', methods=['POST'])
@login_required
def ubanner():
    form = UpdateBannerForm(request.form)
    if form.validate():
        banner_id = form.banner_id.data
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel.query.get(banner_id)
        if banner:
            banner.name = name
            banner.image_url = image_url
            banner.link_url = link_url
            banner.priority = priority
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message="没有找到这个banner")
    else:
        return restful.params_error(message=form.get_error())
@bp.route('/dbanner/', methods=['POST'])
@login_required
def dbanner():
    banner_id = request.form.get('banner_id')
    if not banner_id:
        return restful.params_error(message="请传入轮播图id")

    banner = BannerModel.query.get(banner_id)
    if not banner:
        return restful.params_error(message="没有找到这个轮播图")

    db.session.delete(banner)
    db.session.commit()
    return restful.success()




class LoginView(views.MethodView):
    def get(self, message=None):
        return render_template('cms/cms_login.html', message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remeber = form.remeber.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[config.CMS_USER_ID] = user.id
                if remeber:  # 31天
                    session.permanent = True
                return redirect(url_for('cms.index'))
            else:
                # return restful.params_error(message=form.get_error())
                return self.get(message="邮箱或密码错误")

        else:
            # print(form.errors)
            # if 'email' in form.errors.keys():
            #     message = form.errors['email'][0]
            #     return self.get(message=message)
            # else:
            #     message = form.errors['password'][0]
            #     return self.get(message=message)
            message = form.get_error()
            return self.get(message=message)
            # return restful.params_error(form.get_error())


@bp.route('/logout')
@login_required
def logout():
    del session[config.CMS_USER_ID]
    return redirect(url_for('cms.login'))


class ResetPwdView(views.MethodView):
    # 类属性写装饰器
    decorators = [login_required]

    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        form = ResetpwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user
            if user.check_password(oldpwd):
                if oldpwd == newpwd:
                    return restful.params_error("旧密码与新密码相同，请重新输入")
                else:
                    user.password = newpwd
                    db.session.commit()
                    # {"code":200,message="密码错误"}
                    # return jsonify({"code": 200, "message": "密码修改成功"})
                    return restful.success(data={"修改后密码为": newpwd})
            else:
                print(form.errors)
                return restful.params_error("旧密码输入错误")
                # return jsonify({"code":400, "message":"旧密码错误！"})
        else:
            # print(form.errors)
            # message = form.get_error()
            # return jsonify({"code":400, "message":message})
            return restful.params_error(form.get_error())


class ResetEmail(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('cms/cms_resetemail.html')

    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_error())


@bp.route('/profile')
@login_required
def profile():
    return render_template('cms/cms_profile.html')


@bp.route('/email_captcha/')
def email_captcha():
    email = request.args.get('email')
    if not email:
        return restful.params_error("请输入邮箱")

    source = list(string.ascii_letters)
    # source.extend(map(lambda x:str(x), range(0, 10)))
    source.extend(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])
    captcha = "".join(random.sample(source, 6))

    # 发送邮件
    # message = Message('python论坛邮箱修改验证码',
    #                       recipients=[email],
    #                       body="您的验证码是:%s" % captcha)
    # try:
    #     mail.send(message)
    # except:
    #     return restful.server_error()
    # 异步
    send_mail.delay('python论坛邮箱修改验证码', [email], "您的验证码是:%s" % captcha)
    zlcache.set(email, captcha)
    return restful.success()




# @bp.route('/email/')
# def send_email():
#     message = Message('邮件发送', recipients=['605775776@qq.com'], body='测试')
#     mail.send(message)
#     return 'success'


bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/', view_func=ResetPwdView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/', view_func=ResetEmail.as_view('resetemail'))
