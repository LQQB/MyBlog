from flask_bcrypt import Bcrypt       # 提供 Bcrypt 哈希算法 单向加密方法
#from flask_oauthlib import OAuth
from flask_login import LoginManager  #  Flask 提供用户 session 的管理机制
from flask_principal import  Principal, Permission, RoleNeed, UserNeed
from flask_celery import Celery         # celery 实现异步任务
from flask_mail import Mail
from flask_cache import Cache       # 网页缓存
from flask_assets import Environment, Bundle # 压缩 css/js
from flask_admin import  Admin
from flask_babelex import Babel # 国际化 工具包

bcrypt = Bcrypt()
login_manger = LoginManager()
principal = Principal()
flask_celery = Celery()
mail = Mail()
cache = Cache()
assets_env = Environment()
flask_admin = Admin(name='后台管理系统')
flask_babel = Babel()

# oauth = OAuth
#
# QQ = oauth.remote_app(
#     'QQ',
#     base_url='https://graph.qq.com/oauth2.0/authorize'
# )


login_manger.login_view = 'main.login'
login_manger.session_protection = 'strong'
login_manger.login_message = u'请登录'
login_manger.login_message_category = 'info'

@login_manger.user_loader
def load_user(user_id):
    from LQBBlog.models import User
    return User.query.filter_by(id=user_id).first()

# 设定了 3 种权限, 这些权限被绑定到 Identity 之后才会发挥作用.
admin_permission = Permission(RoleNeed('admin'))
poster_permission = Permission(RoleNeed('poster'))
default_permission = Permission(RoleNeed('default'))

main_css = Bundle(
    'css/bootstrap.min.css',
    'css/bootstrap-theme.min.css',
    filters='cssmin',
    output='assets/css/common.css'  # 打包后的包文件的存放路径
)

main_js = Bundle(
    'js/bootstrap.min.js',
    filters='jsmin',
    output='assets/js/common.js'
)