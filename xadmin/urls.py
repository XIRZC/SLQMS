from django.urls import path

from . import views

app_name = 'xadmin'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('val/', views.val, name='val'),
]