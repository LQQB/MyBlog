from flask import Flask,redirect, url_for

from LQBBlog.config import DevConfig
from LQBBlog.controllers import blog, main
from LQBBlog.models import db
from LQBBlog.extensions import bcrypt

def create_app(object_name):

    app = Flask(__name__)

    # 使用 onfig.from_object() 而不使用 app.config['DEBUG'] 是因为这样可以加载
    # class DevConfig 的配置变量集合，而不需要一项一项的添加和修改。
    app.config.from_object(object_name)

    db.init_app(app)
    
    bcrypt.init_app(app)

    app.register_blueprint(blog.blog_blueprint)
    app.register_blueprint(main.main_blueprint)

    return app
