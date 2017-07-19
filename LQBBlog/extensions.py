from flask_bcrypt import Bcrypt       # 提供 Bcrypt 哈希算法 单向加密方法
#from flask_oauthlib import OAuth
from flask_login import LoginManager  #  Flask 提供用户 session 的管理机制

bcrypt = Bcrypt()

# oauth = OAuth
#
# QQ = oauth.remote_app(
#     'QQ',
#     base_url='https://graph.qq.com/oauth2.0/authorize'
# )

login_manger = LoginManager()
login_manger.login_view = 'main.login'
login_manger.session_protection = 'strong'
login_manger.login_message = 'Please login to access this page.'
login_manger.login_message_category = 'info'

@login_manger.user_loader
def load_user(user_id):
    print('---------------')
    from LQBBlog.models import User
    return User.query.filter_by(id=user_id).first()

