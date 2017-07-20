import datetime
from os import path
from  uuid import uuid4

from flask import render_template, Blueprint, redirect, url_for, flash
from sqlalchemy import func

from LQBBlog.forms import CommentForm, PostForm
from LQBBlog.models import db, User, Post, Tag, Comment, posts_tags
from flask_login import login_required, current_user


blog_blueprint = Blueprint(
    'blog',
    __name__,
    template_folder = path.join(path.pardir, 'templates', 'blog'),
    url_prefix= '/blog')


def sidebar_data():
    recent = db.session.query(Post).order_by(
        Post.publish_date.desc()
    ).limit(5).all()

    top_tags = db.session.query(
        Tag, func.count(posts_tags.c.post_id).label('total')
    ).join(
        posts_tags
    ).group_by(Tag).order_by('total DESC').limit(5).all()
    return recent, top_tags

@blog_blueprint.route('/')
@blog_blueprint.route('/<int:page>')
def home(page=1):
    posts = Post.query.order_by(
        Post.publish_date.desc()
    ).paginate(page, 10)
    recent, top_tags = sidebar_data()
    return render_template('home.html',
                           posts=posts,
                           recent=recent,
                           top_tags=top_tags)

@blog_blueprint.route('/post/<string:post_id>',  methods=('GET', 'POST') )
def post(post_id):
    form = CommentForm()
    if form.validate_on_submit() :
        new_Commnet = Comment(id=str(uuid4()), name=form.name.data)
        new_Commnet.text = form.text.data
        new_Commnet.date = datetime.datetime.now()
        new_Commnet.post_id = post_id
        db.session.add(new_Commnet)
        db.session.commit()



    post = db.session.query(Post).get_or_404(post_id)
    tags = post.tags
    coments = post.comments.order_by(Comment.date.desc()).all()

    recent, top_tags = sidebar_data()

    return render_template('post.html',
                           post=post,
                           tags=tags,
                           coments=coments,
                           form=form,
                           recent=recent,
                           top_tags=top_tags)


@blog_blueprint.route('/tag/<string:tag_name>')
def tag(tag_name):
    """View function for tag page"""

    tag = db.session.query(Tag).filter_by(name=tag_name).first_or_404()
    posts = tag.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template('tag.html',
                           tag=tag,
                           posts=posts,
                           recent=recent,
                           top_tags=top_tags)


@blog_blueprint.route('/user/<string:username>')
def user(username):
    """View function for user page"""
    user = db.session.query(User).filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template('user.html',
                           user=user,
                           posts=posts,
                           recent=recent,
                           top_tags=top_tags)

@blog_blueprint.route('/new', methods=['GET', 'POST'])
@login_required     # 该注解的页面 不能够被匿名用户查看
def new_post():
    form = PostForm()

    if not current_user:     # 代理对象 current_user 来访问和表示当前登录的对象,
        return  redirect(url_for('main.login'))

    if form.validate_on_submit():
        new_post = Post(id=str(uuid4()), title=form.title.data)
        new_post.text = form.text.data
        new_post.publish_date = datetime.datetime.now()
        new_post.users = current_user

        db.session.add(new_post)
        db.session.commit()

        return  redirect(url_for('blog.home'))

    return render_template('new_post.html',
                           form=form)

@blog_blueprint.route('/edit/<string:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):

    post = Post.query.get_or_404(id)


    if not post.user_id == current_user.id :
        flash('文章仅本人可以修改', category='success')
        return  redirect(url_for('blog.home'))

    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.text = form.text.data
        post.publish_date = datetime.datetime.now()

        # 修改 文章
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('blog.post', post_id=post.id))

    return render_template('edit_post.html',
                           form=form,
                           post=post)


