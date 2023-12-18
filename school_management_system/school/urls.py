from django.urls import path
from school import views

urlpatterns = [

    path('', views.admin_register, name='admin_register'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('students/', views.students, name='students'),
    path('register_student/', views.register_student, name='register_student'),
    path('student_status/<int:id>', views.student_status, name='student_status'),
    path('student_login/', views.student_login, name='student_login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('class/', views.all_class, name='class'),
    path('add_class/', views.add_class, name='add_class'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
]
