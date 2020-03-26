from django.urls import path
from student import views

app_name = 'student'

urlpatterns = [
    path('', views.index, name='index'),
    path('student/register/', views.registerView, name='register'),
    path('student/login/', views.loginView, name='login'),
    path('student/logout/', views.logoutView, name='logout'),
    path('student/update/', views.updateView, name='update'),
    path('student/subjects/', views.subjectView, name='subjects')
    #path('routine/', views.routine, name='routine'),
]