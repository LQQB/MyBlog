from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import  DataRequired, Length


class CommentForm(FlaskForm):

    name = StringField(
        'Name',
        validators = [DataRequired(), Length(max=255)]  )

    text = TextAreaField(
        'Comment',
        description = u'请提出宝贵意见和建议',
        validators = [DataRequired()],
        render_kw= {"placeholder": "评论。。。"}  )
