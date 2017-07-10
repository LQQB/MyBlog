from flask import Flask
from config import  DevConfig

app = Flask(__name__)

app.config.from_object(DevConfig)

@app.route('/')
def hello():
    return 'hello world'

if __name__ == '__main__':
    app.run()