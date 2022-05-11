from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from xadmin.models import Teacher, Class, Student
from xadmin.serializers import TeacherSerializer, ClassSerializer, StudentSerializer

from rest_framework import viewsets
from rest_framework.response import Response

# Create your views here.

class LoginView(generic.ListView):
    template_name = 'xadmin/login.html'
    model = Student

def val(request):
    id = request.POST['username']
    pwd = request.POST['password']
    role = request.POST['role']
    if role == 'student':
        try:
            s = Student.objects.get(id=id)
            if pwd == s.pwd:
                return redirect('/student/{}/'.format(s.id))
                # return HttpResponse("登录成功!")
            else:
                return HttpResponse("密码不正确,登录失败!")
        except (KeyError, Student.DoesNotExist):
            return HttpResponse("用户不存在, 请重新输入信息后登录!")
    else:
        try:
            t = Teacher.objects.get(id=id)
            if pwd == t.pwd:
                return redirect('/teachclass/{}/'.format(t.id))
                # return HttpResponse("登录成功!")
            else:
                return HttpResponse("密码不正确,登录失败!")
        except (KeyError, Student.DoesNotExist):
            return HttpResponse("用户不存在, 请重新输入信息后登录!")

def TeachClassView(request, tid):
    t = get_object_or_404(Teacher, pk=tid)
    t.info = '{}-{}'.format(t.id, t.name)
    return render(request, 'xadmin/teachclass.html', {'teacher': t})

def TeachClassAPI(request, tid):
    classes = Class.objects.filter(tid=tid)
    serializer =  ClassSerializer(classes, many=True)
    data = {
        "code": 0,
        "msg": "",
        "count": len(serializer.data),
        "data": serializer.data,
    }
    return JsonResponse(data, safe=True)

def TeachStudentTableView(request, tid, cid):
    t = get_object_or_404(Teacher, pk=tid)
    t.info = '{}-{}'.format(t.id, t.name)
    c = get_object_or_404(Class, pk=cid)
    return render(request, 'xadmin/teachstudenttable.html', {'teacher': t, 'class': c})
def TeachStudentChartView(request, tid, cid):
    t = get_object_or_404(Teacher, pk=tid)
    t.info = '{}-{}'.format(t.id, t.name)
    c = get_object_or_404(Class, pk=cid)
    return render(request, 'xadmin/teachstudentchart.html', {'teacher': t, 'class': c})

def StudentView(request, sid):
    s = get_object_or_404(Teacher, pk=sid)
    s.info = '{}-{}-{}'.format(s.id, s.name, s.cid.name)
    print('student', s.id)
    return render(request, 'xadmin/student.html', {'student': s})

def StudentAPI(reqeust, cid):
    students = Student.objects.filter(cid=cid)
    serializer = StudentSerializer(students, many=True)
    data = {
        "code": 0,
        "msg": "",
        "count": len(serializer.data),
        "data": serializer.data,
    }
    return JsonResponse(data, safe=True)

class StudentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
class TeacherViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
class ClassViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Class.objects.all()
    serializer_class = ClassSerializer