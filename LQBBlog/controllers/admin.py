from flask_admin import BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from LQBBlog.forms import CKTextAreaField
from flask_login import login_required, current_user
from LQBBlog.extensions import admin_permission

class HomeView(AdminIndexView) :

    @login_required
    @admin_permission.require(http_exception=403)
    @expose('/')
    def index(self):
        return self.render('admin/welcome.html')


    #
    # @expose('/second_page')
    # def second_page(self):
    #     return self.render('admin/second_page.html')

class CustomModelView(ModelView):

    # 设置 ModelAdmin 和 FileAdmin 子类的访问权限, 需要为它们定义一个 is_accessible() function,
    # 并且返回的值必须为 Bool 类型对象, 至于权限的设置模式由我们自己定义.
    def is_accessible(self):
        return current_user.is_authenticated() and\
            admin_permission.can()



class PostView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated() and\
            admin_permission.can()
    # can_create = False  #

    form_overrides = dict(text=CKTextAreaField)

    column_searchable_list = ('text', 'title')
    column_filters = ('publish_date',)


    create_template = 'admin/post_edit.html'
    edit_template = 'admin/post_edit.html'


class SysImagesAdmin(FileAdmin):
    '''
        图片 文件管理
    '''
    def is_accessible(self):
        return current_user.is_authenticated() and\
            admin_permission.can()

    can_mkdir = False



    allowed_extensions = ('jpg', 'gif', 'png')
    list_template = 'admin/file_list_Images.html'
    pass


class SysPDFAdmin(FileAdmin):
    '''
        PDF 文件管理
    '''
    def is_accessible(self):
        return current_user.is_authenticated() and\
            admin_permission.can()

    can_mkdir = False


    allowed_extensions = ( 'pdf')
    list_template = 'admin/file_list_PDF.html'