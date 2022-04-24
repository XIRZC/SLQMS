from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone

from .models import User
# Create your views here.

class IndexView(generic.ListView):
    template_name = 'xadmin/index.html'

    def get_queryset(self): 
        """
        get all users
        """
        return User.objects.all()


class LoginView(generic.ListView):
    template_name = 'xadmin/login.html'
    model = User

    # def get_queryset(self): 
    #     """
    #     get all users
    #     """
    #     return User.objects.all()

def val(request):
    uid = request.POST['username']
    upwd = request.POST['password']
    try:
        u = User.objects.get(uid=uid)
        if upwd == u.upwd:
            return HttpResponse("登录成功!")
        else:
            return HttpResponse("密码不正确,登录失败!")
    except (KeyError, User.DoesNotExist):
        return HttpResponse("用户不存在, 请重新输入信息后登录!")