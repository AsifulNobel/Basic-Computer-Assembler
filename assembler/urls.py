from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.upload_file, name='file_upload'),
]
