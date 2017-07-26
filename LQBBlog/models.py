from flask_sqlalchemy import SQLAlchemy
from LQBBlog.extensions import bcrypt
from flask_login import UserMixin,AnonymousUserMixin

# SQLAlchemy 会自动的从 app 对象中的 DevConfig 中加载连接数据库的配置项
db = SQLAlchemy()

users_roles = db.Table('users_roles',
                      db.Column('user_id', db.String(45), db.ForeignKey('t_user.id')),
                      db.Column('role_id', db.String(45), db.ForeignKey('t_role.id')) )

class User(db.Model):

    __tablename__ = 't_user'
    id = db.Column(db.String(45), primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    # 定义 1 对 多 关系
    posts = db.relationship(
        'Post',
        backref='t_user',
        lazy='dynamic'
    )

    roles = db.relationship(
        'Role',
        secondary=users_roles,
        backref=db.backref('t_user', lazy='dynamic')
    )

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = self.set_password(password)

    # 被默认调用. 与 repr() 类似, 将对象转化为便于供 Python 解释器读取的形式,
    # 返回一个可以用来表示对象的可打印字符串.
    def __repr__(self):
        """Define the string format for instance of User."""
        return "<Model User `{}`>".format(self.username)

    # 给密码加密
    def set_password(self, password):
        return bcrypt.generate_password_hash(password)

    # 密码校验
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


    def is_authenticated(self):
        # if isinstance(self, AnonymousUserMixin):
        #     return False
        # else:
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        # if isinstance(self, AnonymousUserMixin):
        #     return True
        # else:
        return False

    def get_id(self):
        """Get the user's uuid from database."""
        return self.id.encode('unicode-escape')

class Role(db.Model) :

    __tablename__ = 't_role'
    id = db.Column(db.String(45), primary_key=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, id, name):
        self.id = id
        self.name = name


    def __repr__(self):
        return '<Model Role {}>'.format(self.name)

posts_tags = db.Table('posts_tags',
                      db.Column('post_id', db.String(45), db.ForeignKey('t_post.id')),
                      db.Column('tag_id', db.String(45), db.ForeignKey('t_tag.id')) )

class Post(db.Model):

    __tablename__ = 't_post'
    id = db.Column(db.String(45), primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime)
    user_id = db.Column(db.String(45), db.ForeignKey('t_user.id'))  # 外键约束

    comments = db.relationship( # 定义 1 对 多 关系
        'Comment',
        backref='t_post',
        lazy='dynamic')

    tags = db.relationship(    # 定义 多 对 多 关系
        'Tag',
        secondary = posts_tags,
        backref = db.backref('t_post', lazy='dynamic')
    )

    def __init__(self,id, title):
        self.id = id
        self.title = title

    def __repr__(self):
        return "<Model Post `{}`>".format(self.title)
# if __name__ == '__main__':
#      user = User('LQB')
#      print(user)
#      print(user.id)

class Tag(db.Model) :
    __tablename__ = 't_tag'
    id = db.Column(db.String(45), primary_key=True)
    name = db.Column(db.String(255))

    def __init__(self,id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return '<Model Comment `{}`>'.format(self.name)

class Comment(db.Model) :

    __tablename__ = 't_comment'
    id =db.Column(db.String(45), primary_key=True)
    name = db.Column(db.String(255))
    text = db.Column(db.Text())
    date = db.Column(db.DateTime())
    post_id = db.Column(db.String(45), db.ForeignKey('t_post.id'))

    def __init__(self,id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return '<Model Comment `{}`>'.format(self.name)

class Reminder(db.Model) :
    __tablename__ = 't_reminders'
    id = db.Column(db.String(45), primary_key=True)
    date = db.Column(db.DateTime())
    email = db.Column(db.String(255))
    text = db.Column(db.Text())

    def __init__(self, id, text):
        self.id = id
        self.text = text

    def __repr__(self):
        return '<Model Reminder `{}`>'.format(self.text[:20])
