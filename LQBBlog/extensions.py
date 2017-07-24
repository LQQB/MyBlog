from flask_bcrypt import Bcrypt       # 提供 Bcrypt 哈希算法 单向加密方法
#from flask_oauthlib import OAuth
from flask_login import LoginManager  #  Flask 提供用户 session 的管理机制
from flask_principal import  Principal, Permission, RoleNeed, UserNeed

bcrypt = Bcrypt()
login_manger = LoginManager()
principal = Principal()
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