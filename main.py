from flask import Flask
from config import  DevConfig

app = Flask(__name__)


# 使用 onfig.from_object() 而不使用 app.config['DEBUG'] 是因为这样可以加载
# class DevConfig 的配置变量集合，而不需要一项一项的添加和修改。
app.config.from_object(DevConfig)

@app.route('/')
def hello():
    return '<h1>hello world</ht1>'

if __name__ == '__main__':
    app.run()