from flask_admin import BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from LQBBlog.forms import CKTextAreaField

# class CustomView(BaseView) :
#
#     @expose('/')
#     def index(self):
#         return self.render('admin/custom.html')
#
#
#     @expose('/second_page')
#     def second_page(self):
#         return self.render('admin/second_page.html')

class CustomModelView(ModelView):

    pass


class PostView(ModelView):
    # can_create = False  #

    form_overrides = dict(text=CKTextAreaField)

    column_searchable_list = ('text', 'title')
    column_filters = ('publish_date',)


    create_template = 'admin/post_edit.html'
    edit_template = 'admin/post_edit.html'


class SysFileAdmin(FileAdmin):

    can_mkdir = False
    can_upload = False
    can_delete = False
    can_rename = False


    allowed_extensions = ('swf', 'jpg', 'gif', 'png', 'pdf')
    list_template = 'admin/file_list.html'
    pass