from flask import Flask,redirect, url_for

from LQBBlog.config import DevConfig
from LQBBlog.controllers import blog
from LQBBlog.models import db
app = Flask(__name__)

# 使用 onfig.from_object() 而不使用 app.config['DEBUG'] 是因为这样可以加载
# class DevConfig 的配置变量集合，而不需要一项一项的添加和修改。
app.config.from_object(DevConfig)

db.init_app(app)

@app.route('/')
def index():
    return redirect(url_for('blog.home'))

app.register_blueprint(blog.blog_blueprint)

if __name__ == '__main__':

    app.run()