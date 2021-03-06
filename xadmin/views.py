from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings

from xadmin.models import Teacher, Class, Student
from xadmin.serializers import TeacherSerializer, ClassSerializer, StudentSerializer

from rest_framework import viewsets
from rest_framework.response import Response

import sklearn
import pandas as pd
import seaborn as sb
import numpy as np
import joblib
import json

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
        except (KeyError, Teacher.DoesNotExist):
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
    students = Student.objects.filter(id=sid)
    students = inference(students)
    s = students[0]
    s.info = '{}-{}-{}'.format(s.id, s.name, s.cid.name)
    return render(request, 'xadmin/student.html', {'student': s})

def inference(query_sets):
    print(type(query_sets))
    models_root = settings.STATIC_ROOT / 'models'
    with (models_root / 'cfgs.json').open() as f:
        cfgs = json.load(f)
        if cfgs['mode'] == 'LR':
            model = joblib.load(models_root / 'lr.pkl')
        elif cfgs['mode'] == 'SVM':
            model = joblib.load(models_root / 'svm.pkl')
        else:  # MLP
            model = joblib.load(models_root / 'mlp.pkl')
        
        dataframe = pd.DataFrame(list(query_sets.values())).iloc[:, 3:11]
    levels = model.predict(dataframe)
    # print('levels', levels)
    id2level = {
        '0': 'A',
        '1': 'B',
        '2': 'C'
    }
    id2advice = {
        '0': '学习质量高，请继续以同样方法和步幅坚持学习，祝你最后期末取得佳绩',
        '1': '学习质量一般，请尝试根据自身不足多加复习，查漏补缺，及时调整学习步幅和方法有助于提高学习质量',
        '2': '学习质量较差，若继续以过往步幅和方法进行学习，将很有可能导致期末分数不及格，请迅速做出更改，努力学习',
    }
    for i, s in enumerate(query_sets):
        s.level = id2level[str(levels[i])]
        s.advice = id2advice[str(levels[i])]
    return query_sets


def StudentAPI(reqeust, sid):
    students = Student.objects.filter(id=sid)
    students = inference(students)
    serializer = StudentSerializer(students, many=True)
    data = {
        "code": 0,
        "msg": "",
        "count": len(serializer.data),
        "data": serializer.data,
    }
    return JsonResponse(data, safe=True)
def StudentsAPI(reqeust, cid):
    students = Student.objects.filter(cid=cid)
    students = inference(students)
    serializer = StudentSerializer(students, many=True)
    cnts = {
        'A': 0,
        'B': 0,
        'C': 0,
    }
    for s in students:
        cnts[s.level] += 1
    # stat = {
    #     'categories': ['优秀', '良好', '不合格'],
    #     'values': [cnts['A'] * 100 // len(students),\
    #         cnts['B'] * 100 // len(students), cnts['C'] * 100 // len(students)]
    # }
    stat = [
        {'value': cnts['A'] * 100 // len(students), 'name': '优秀'},
        {'value': cnts['B'] * 100 // len(students), 'name': '良好'},
        {'value': cnts['C'] * 100 // len(students), 'name': '不合格'},
    ]
    data = {
        "code": 0,
        "msg": "",
        "count": len(serializer.data),
        "statistics": stat,
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