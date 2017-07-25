import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server  # 最新2.0.5版本改了语法

from LQBBlog import models, create_app


env = os.environ.get('flakWeb', 'dev')
print('LQBBlog.config.%sConfig' %env.capitalize())
app = create_app('LQBBlog.config.%sConfig' %env.capitalize())


manager = Manager(app)

migrate = Migrate(app, models.db)

manager.add_command('server', Server(host='127.0.0.1', port=5000) )
manager.add_command('db', MigrateCommand)

@manager.shell
def make_shell_context():
    # 我们 每在 models.py 中新定义一个数据模型, 都需要在 manager.py 中导入并添加到返回 dict 中.
    return dict(app=app,
                db=models.db,
                User=models.User,
                Post=models.Post,
                Comment=models.Comment,
                Tag=models.Tag,
                Role=models.Role,
                Server=Server)

# 通过 manager.py 来执行命令行是十分有必要lask app object 时，直接运行默认的 python CLI 会导致这些 Flask 扩展返回错误。
if __name__ == '__main__':
    manager.run()