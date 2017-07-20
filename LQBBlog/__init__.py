from flask import Flask,redirect, url_for

from LQBBlog.config import DevConfig
from LQBBlog.controllers import blog, main
from LQBBlog.models import db
from LQBBlog.extensions import bcrypt,login_manger

def create_app(object_name):

    app = Flask(__name__)       # Flask类的实例 app

    # 使用 onfig.from_object() 而不使用 app.config['DEBUG'] 是因为这样可以加载
    # class DevConfig 的配置变量集合，而不需要一项一项的添加和修改。
    app.config.from_object(object_name)

    db.init_app(app)
    
    bcrypt.init_app(app)    #  将 extensions 中的  Flask 扩展， 初始化 绑定到 app 中
    login_manger.init_app(app)

    app.register_blueprint(blog.blog_blueprint)
    app.register_blueprint(main.main_blueprint)

    return app
