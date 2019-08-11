from django.urls import path, include
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('', views.Home, name='Home'),
    path('admin', views.AdminLogin, name='AdminLogin'),
    path('uploader', views.FileuploaderLogin, name='FileuploaderLogin'),
    path('recepient', views.FilerecepientLogin, name='FilerecepientLogin'),
    path('api/uploaderlogin', views.UploaderLoginFunc, name='UploaderLoginFunc'),
    path('api/recipientlogin', views.RecipientLoginFunc, name='RecipientLoginFunc'),
    path('api/fileupload', views.FileUpload, name='FileUploadFunc'),
    path('api/filelog', views.FileLog, name='FileLogFunc'),
    path('api/fileview', views.FileView, name='FileViewFunc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
