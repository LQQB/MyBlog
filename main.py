from flask import Flask,render_template
from config import  DevConfig

app = Flask(__name__)
views = __import__('views')

# 使用 onfig.from_object() 而不使用 app.config['DEBUG'] 是因为这样可以加载
# class DevConfig 的配置变量集合，而不需要一项一项的添加和修改。
app.config.from_object(DevConfig)

if __name__ == '__main__':
    app.run()