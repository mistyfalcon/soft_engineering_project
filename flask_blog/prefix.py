
# -*- coding:utf8 -*-

# 从app模块中导入app应用
from app import app, db
from app.models import User, Post
# 防止被引用后执行，只有在当前模块中才可以使用


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}