from flask import Flask
from config import  DevConfig

app = Flask(__name__)

app.config.from_object(DevConfig)

@app.route('/')
def hello():
    return '<h1>hello world</ht1>'

if __name__ == '__main__':
    app.run()