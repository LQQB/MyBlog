import datetime
import random
from uuid import uuid4

from LQBBlog.models import db, User, Tag, Post

user = User(id=(str(uuid4())), username='LQB', password='123456')
db.session.add(user)
db.session.commit()

user0 = db.session.query(User).first()

tag_one = Tag(id=(str(uuid4())), name = 'Python')
tag_two = Tag(id=(str(uuid4())), name = 'Java')
tag_three = Tag(id=(str(uuid4())), name = 'Go')
tag_four = Tag(id=(str(uuid4())),name= '玄学')
Tags = [tag_one, tag_two, tag_three, tag_four]


Text = u'放空自己 ╮(╯_╰)╭  一片空白~~~~~~~~~~~~~~~'

for i in range(100):
    new_Post = Post(id=str(uuid4()), title='Post'+str(i))
    new_Post.user_id = user0.id
    new_Post.publish_date = datetime.datetime.now()
    new_Post.text = Text
    new_Post.tags = random.sample(Tags, random.randint(1,3)) # # 从list中随机获取5个元素，作为一个片断返回
    db.session.add(new_Post)

db.session.commit()