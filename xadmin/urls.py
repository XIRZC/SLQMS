from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from django.urls import path

from xadmin import views

app_name = 'xadmin'

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'teachers', views.TeacherViewSet)
router.register(r'classes', views.ClassViewSet)
router.register(r'students', views.StudentViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    path('login/', views.LoginView.as_view(), name='login'),
    path('val/', views.val, name='val'),
    path('teachclass/<int:tid>/', views.TeachClassView, name='teachclass'),
    path('teachclassapi/<int:tid>/', views.TeachClassAPI, name='teachclassapi'),
    path('teachclass/<int:tid>/class/<int:cid>/table/', views.TeachStudentTableView, name='teachstudenttable'),
    path('teachclass/<int:tid>/class/<int:cid>/chart/', views.TeachStudentChartView, name='teachstudentchart'),
    path('student/<int:sid>/', views.StudentView, name='student'),
    path('studentapi/<int:sid>/', views.StudentAPI, name='studentapi'),
    path('studentsapi/<int:cid>/', views.StudentsAPI, name='studentsapi'),
]