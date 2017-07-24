from uuid import uuid4
from os import path

from flask import render_template, Blueprint, redirect, url_for, flash
from LQBBlog.models import db, User
from LQBBlog.forms import LoginForm, RegisterForm
from flask_login import login_user, logout_user
from flask_principal import Identity, identity_changed, current_app, AnonymousIdentity

main_blueprint = Blueprint(
    'main',
    __name__,
    template_folder=path.join(path.pardir, 'templates', 'main'))


@main_blueprint.route('/')
def index():
    return redirect(url_for('blog.home'))

@main_blueprint.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():   # validate_on_submit 这个方法 会调用 self.is_submitted() and self.validate() ，
                                    # 为了校验用户名密码是否正确，在 class LoginForm 重写了 validate() 这个方法

        user = User.query.filter_by(username=form.username.data).first()

        login_user(user, remember=form.remember.data)   # login_user 能够将已登录并通过 load_user() 的用户对应的 User 对象, 保存在 session 中

        identity_changed.send(  # 表示应用 app 对象中的 user 用户对象的 identity 被改变了.
            current_app._get_current_object(), # current_app : 当前应用对象 app
            identity = Identity(user.id))      # identity :　身份对象 Id

        flash('您已登录', category='success')
        return redirect(url_for('blog.home'))

    return  render_template('login.html',
                                form=form)

@main_blueprint.route('/logout', methods=['POST', 'GET'])
def logout():

    logout_user()

    identity_changed.send(
        current_app._get_current_object(),
        identity = AnonymousIdentity()) # 用户登出系统后清理 session，Flask-Principal 会将用户的身份变为 AnonymousIdentity(匿名身份)

    flash('你已经注销了', category='success')
    return redirect(url_for('main.login'))

@main_blueprint.route('/register', methods=['POST', 'GET'])
def register():

    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(id=str(uuid4()),
                        username=form.username.data,
                        password=form.password.data)

        db.session.add(new_user)
        db.session.commit()

        flash('您已注册成功', category='success')

        return redirect(url_for('main.login'))

    return render_template('register.html',
                           form=form)