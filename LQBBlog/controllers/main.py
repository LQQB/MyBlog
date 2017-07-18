from uuid import uuid4
from os import path

from flask import render_template, Blueprint, redirect, url_for, flash
from LQBBlog.models import db, User, Post, Tag, Comment, posts_tags
from LQBBlog.forms import LoginForm, RegisterForm


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
    if form.validate_on_submit():
        flash('您已登录', category='success')
        return redirect(url_for('blog.home'))

    return  render_template('login.html',
                                form=form)

@main_blueprint.route('/logout', methods=['POST', 'GET'])
def logout():

    flash('你已经注销了', category='success')
    return redirect('blog.home')

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