from django.contrib import admin
from .models import *
# Register your models here.


class CustomuserAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type')


class FilemanagerAdmin(admin.ModelAdmin):
    list_display = ('file_uploader', 'file_recepient', 'file')


admin.site.register(CustomUser, CustomuserAdmin)
admin.site.register(FileManager, FilemanagerAdmin)


admin.site.site_header = 'File Upload'
