import os
from LQBBlog import models, create_app

env = os.environ.get('flakWeb', 'dev')
app = create_app('LQBBlog.config.%sConfig' %env.capitalize())

if __name__ == '__main__':
    app.run()