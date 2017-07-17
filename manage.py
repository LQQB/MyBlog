from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server  # 最新2.0.5版本改了语法

from LQBBlog import models, __init__

manager = Manager(__init__.app)

migrate = Migrate(__init__.app, models.SQLAlchemy())

manager.add_command('server', Server() )
manager.add_command('db', MigrateCommand)

@manager.shell
def make_shell_context():
    # 我们 每在 models.py 中新定义一个数据模型, 都需要在 manager.py 中导入并添加到返回 dict 中.
    return dict(app=__init__.app,
                db=models.db,
                User=models.User,
                Post=models.Post,
                Comment=models.Comment,
                Tag=models.Tag)

# 通过 manager.py 来执行命令行是十分有必要的，因为一些 Flask 的扩展只有在 Flask app object 被创建之后才会被初始化，
# 所以非常依赖于应用上下文的环境，在没有 Flask app object 时，直接运行默认的 python CLI 会导致这些 Flask 扩展返回错误。
if __name__ == '__main__':
    manager.run()