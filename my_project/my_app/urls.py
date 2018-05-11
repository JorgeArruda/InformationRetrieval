from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'sendfile$', views.upload_drive, name='upload_drive'),
]
