# encoding: utf-8
import os

# SECRET_KEY = os.urandom(24)
SECRET_KEY = "asdasdafada"

DEBUG = True

DB_USERNAME = 'root'
DB_PASSWORD = 'root'
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'zlbbs'


DB_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (DB_USERNAME,DB_PASSWORD,DB_HOST,DB_PORT,DB_NAME)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

CMS_USER_ID ='dsw'
Front_USER_ID = 'DSW'


# 发送邮件配置
# MAIL_USE_TLS：端口号587
# MAIL_USE_SSL：端口号465
# QQ邮箱不支持非加密方式发送邮件
# 发送者邮箱的服务器地址
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = '587'
MAIL_USE_TLS = True
# MAIL_USE_SSL
MAIL_USERNAME = "605775776@qq.com"
MAIL_PASSWORD = "yudbjuemfwcwbffb"
MAIL_DEFAULT_SENDER = "605775776@qq.com"


# 阿里大于相关配置
# ALIDAYU_APP_KEY = 'LTAI4G7YGK8FPAyu5ojLqyFD'
# ALIDAYU_APP_SECRET = 'EjTWAM3tHCBUEBsEu2xtqDzbLVLHAy'
# ALIDAYU_SIGN_NAME = '小饭桌应用'
# ALIDAYU_TEMPLATE_CODE = 'SMS_68465012'


# UEditor的相关配置
UEDITOR_UPLOAD_TO_QINIU = True
UEDITOR_QINIU_ACCESS_KEY = "A4rwmzix2yRTKQJerrGRxzMBV0qVk3fWkYJ"
UEDITOR_QINIU_SECRET_KEY = "hmrhR--FNC-TN0B4wqIbe6hS2p6w2ZdCTBEvd98t"
UEDITOR_QINIU_BUCKET_NAME = "605775776"
UEDITOR_QINIU_DOMAIN = "http://qgt5u4j99.hd-bkt.clouddn.com/"


# flask-paginate的相关配置
PER_PAGE = 10

# celery相关的配置
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"