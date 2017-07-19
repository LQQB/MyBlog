from flask_wtf import FlaskForm         # flask 提供的 form 表单的校验框架
from wtforms import StringField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import  DataRequired, Length, EqualTo
from LQBBlog.models import db, User


class CommentForm(FlaskForm):
    '''
    评论 校验
    '''
    name = StringField(
        'Name',
        validators = [DataRequired(), Length(max=255)]  )

    text = TextAreaField(
        'Comment',
        description = u'请提出宝贵意见和建议',
        validators = [DataRequired()],
        render_kw= {"placeholder": "评论。。。"}  )

class LoginForm(FlaskForm):

    username = StringField('UserName', [DataRequired(), Length(max=255)])
    password = PasswordField('PassWord', [DataRequired()] )
    remember = BooleanField('Remember Me')

    def validator(self):
        check_validator = super(LoginForm, self).validate()

        if not check_validator:
            return  False

        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append('有户名或密码无效')
            return  False

        if not user.check_password(self.password.data):
            self.username.errors.append('有户名或密码无效')
            return False

        return True

class RegisterForm(FlaskForm):

    username = StringField('UserName', [DataRequired(), Length(max=255)])
    password = PasswordField('PassWord', [DataRequired(), Length(min=8)])
    agin_password = PasswordField('Agin_PassWord', [DataRequired(), EqualTo('password')])

    def validator(self):
        check_validator = super(RegisterForm, self).validate()

        if not check_validator:
            return  False

        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append('有户名或密码无效')
            return False
        return True

class PostForm(FlaskForm):

    title = StringField('Title', [DataRequired(), Length(max=255)])
    text = TextAreaField('Blog Content', [DataRequired()])
