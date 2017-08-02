from flask import Flask,redirect, url_for

from LQBBlog.config import DevConfig
from LQBBlog.controllers import blog, main
from LQBBlog.controllers.admin import CustomModelView, PostView, SysFileAdmin, AdminIndexView

from LQBBlog.models import db, Role, Tag, Reminder, Comment, Post, User
from LQBBlog.extensions import bcrypt, login_manger, principal, flask_celery, cache, \
    assets_env, main_js, main_css, flask_admin
from flask_principal import identity_loaded, UserNeed, RoleNeed
from flask_login import current_user

import os

def create_app(object_name):

    app = Flask(__name__)       # Flask类的实例 app

    # 使用 onfig.from_object() 而不使用 app.config['DEBUG'] 是因为这样可以加载
    # class DevConfig 的配置变量集合，而不需要一项一项的添加和修改。
    app.config.from_object(object_name)

    db.init_app(app)
    
    bcrypt.init_app(app)    #  将 extensions 中的  Flask 扩展， 初始化 绑定到 app 中
    login_manger.init_app(app)
    principal.init_app(app)
    flask_celery.init_app(app)
    cache.init_app(app)

    assets_env.init_app(app)
    assets_env.register('main_css', main_css)
    assets_env.register('main_js', main_js)

    flask_admin.init_app(app)
    # flask_admin.add_view(CustomView(name='自定义'))

    models = [Role, Tag, Reminder, Comment, User] # 给
    models_name = ['角色','标题', '邮件', '评论', '用户']
    for model_index in range(len(models)):
        flask_admin.add_view(
            CustomModelView(models[model_index], db.session, name=models_name[model_index], category='基础管理模块'))

    flask_admin.add_view(PostView(Post, db.session, name='管理文章'))
    flask_admin.add_view(SysFileAdmin(os.path.join(os.path.dirname(__file__), 'static/upload'),
            '/static/upload', name='管理文件'))

    @identity_loaded.connect_via(app)       # 角色权限 设置
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

