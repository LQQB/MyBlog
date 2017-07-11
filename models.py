from flask_sqlalchemy import SQLAlchemy
from main import  app

# SQLAlchemy 会自动的从 app 对象中的 DevConfig 中加载连接数据库的配置项
db = SQLAlchemy(app)

class User(db.Model):

    __tablename__ = 't_user'
    id = db.Column(db.String(45), primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))

    # def __init__(self, username):
    #     self.username = username

    # 被默认调用. 与 repr() 类似, 将对象转化为便于供 Python 解释器读取的形式,
    # 返回一个可以用来表示对象的可打印字符串.
    def __repr__(self):
        """Define the string format for instance of User."""
        return "<Model User `{}`>".format(self.username)

# if __name__ == '__main__':
#      user = User('LQB')
#      print(user)
#      print(user.id)
