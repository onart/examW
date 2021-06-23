from django.urls import include, path, re_path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('',views.redir),
    path('home', views.home, name='home'),
    path('q/<int:qno>',views.question, name='question'),
    path('q/execjs',views.execJS, name='execJS'),
]