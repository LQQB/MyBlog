from flask import Flask,redirect, url_for

from LQBBlog.config import DevConfig
from LQBBlog.controllers import blog, main
from LQBBlog.models import db
from LQBBlog.extensions import bcrypt, login_manger, principal
from flask_principal import identity_loaded, UserNeed, RoleNeed
from flask_login import current_user

def create_app(object_name):

    app = Flask(__name__)       # Flask类的实例 app

    # 使用 onfig.from_object() 而不使用 app.config['DEBUG'] 是因为这样可以加载
    # class DevConfig 的配置变量集合，而不需要一项一项的添加和修改。
    app.config.from_object(object_name)

    db.init_app(app)
    
    bcrypt.init_app(app)    #  将 extensions 中的  Flask 扩展， 初始化 绑定到 app 中
    login_manger.init_app(app)
    principal.init_app(app)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):

        identity.user = current_user

        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))

    app.register_blueprint(blog.blog_blueprint)     # 载入蓝图
    app.register_blueprint(main.main_blueprint)

    return app
