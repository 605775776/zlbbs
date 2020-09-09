from flask import Flask
from apps.cms import bp as cms_bp
from apps.common import bp as common_bp
from apps.front import bp as front_bp
import config
from exts import db, mail
from flask_wtf import CSRFProtect

def create_app():
    app = Flask(__name__)


    # 导入config
    app.config.from_object(config)

    # 注册db
    db.init_app(app)

    # CSRF攻击
    CSRFProtect(app)

    # mail绑定app
    mail.init_app(app)
    # 注册蓝图
    app.register_blueprint(cms_bp)
    app.register_blueprint(front_bp)
    app.register_blueprint(common_bp)

    return app




if __name__ == '__main__':
    app = create_app()
    app.run()
