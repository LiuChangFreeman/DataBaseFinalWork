from django.conf.urls import include, url
from main import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'index', views.index),
    url(r'login', views.login),
    url(r'register', views.register),
    url(r'main', views.main),
    url(r'uploadfile', views.uploadfile)
]
