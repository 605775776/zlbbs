from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from exts import db
from zlbbs import create_app
from apps.cms import models as cms_models
from apps.front import models as front_models
from apps import models as banner_models
from apps.models import BannerModel, BoardModel

app = create_app()
CMSUser = cms_models.CMSUser
CMSRole = cms_models.CMSRole
CMSPermission = cms_models.CMSPermission

FrontUser = front_models.FrontUser

manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)


# 通过命令添加用户

@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-e', '--email', dest='email')
def create_cms_user(username, password, email):
    user = CMSUser(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    print("cms用户添加成功")


@manager.command
def create_role():
    # 访问者 可以修改个人信息
    visitor = CMSRole(name='访问者', desc='访问权限 无修改权限')
    visitor.permissions = CMSPermission.VISITOR

    # 运营人员 修改个人信息 管理帖子 管理评论 管理前台用户
    operator = CMSRole(name='运营', desc='管理帖子 管理评论 管理前台用户')
    operator.permissions = CMSPermission.VISITOR | CMSPermission.POSTER | CMSPermission.COMMENTER | CMSPermission.FRONTUSER

    # 管理员
    admin = CMSRole(name='管理员', desc='拥有所有权限')
    admin.permissions = CMSPermission.VISITOR | CMSPermission.POSTER | CMSPermission.CMSUSER | CMSPermission.COMMENTER | CMSPermission.FRONTUSER | CMSPermission.BOARDER

    # 开发者
    developer = CMSRole(name='开发者', desc='root用户')
    developer.permissions = CMSPermission.ALL_PERMISSION

    db.session.add_all([visitor, operator, admin, developer])
    db.session.commit()


@manager.option('-e', '--email', dest='email')
@manager.option('-n', '--name', dest='name')
def add_user_to_role(email, name):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        role = CMSRole.query.filter_by(name=name).first()
        if role:
            role.users.append(user)
            db.session.commit()
            print("用户添加到角色成功")

        else:
            print("没有 %s 角色" % role)
    else:
        print("%s没有该用户" % email)


@manager.option('-t', '--telephone', dest='telephone')
@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
def create_front_user(telephone, username, password):
    user = FrontUser(telephone=telephone, username=username, password=password)
    db.session.add(user)
    db.session.commit()
    print("Front用户添加成功")


@manager.command
def test_permission():
    user = CMSUser.query.first()
    # if user.has_permission(CMSPermission.VISITOR):
    if user.is_developer:
        print("{} 拥有访问者权限".format(user))
    else:
        print("{} 没有访问者权限".format(user))





if __name__ == '__main__':
    manager.run()
