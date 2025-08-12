from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import (student_profile_view,
                    student_profile_edit, student_profile,
                    teacher_profile, edit_teacher_profile, secure_logout,
                    StudentPasswordChangeView, TeacherPasswordChangeView,
                    institute_dashboard, institute_profile, admin_dashboard)

urlpatterns = [
    path('', views.home, name='home'),  # Homepage
    path('signup/student/', views.student_signup, name='student_signup'),
    path('signup/teacher/', views.teacher_signup, name='teacher_signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', secure_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('institute/dashboard/', views.institute_dashboard, name='institute_dashboard'),
    path('student/profile/', student_profile_view, name='student_profile'),
    path('profile/student/', student_profile, name='student_profile'),
    path('profile/student/edit/', student_profile_edit, name='student_profile_edit'),
    path('profile/teacher/', views.teacher_profile, name='teacher_profile'),
    path('profile/teacher/edit/', views.edit_teacher_profile, name='edit_teacher_profile'),
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change'),
    path('profile/institute/', views.institute_profile, name='institute_profile'),
    path('profile/institute/edit/', views.edit_institute_profile, name='edit_institute_profile'),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    
]

urlpatterns += [
    path('student/profile/edit/', student_profile_edit, name='edit_student_profile'),
]

urlpatterns += [
    path('student/password-change/', 
        StudentPasswordChangeView.as_view(), 
        name='student_password_change'),

    path('teacher/password-change/', 
        TeacherPasswordChangeView.as_view(), 
        name='teacher_password_change'),

]

urlpatterns += [
    path('profile/institute/', institute_profile, name='institute_profile'),
    path('dashboard/institute/', institute_dashboard, name='institute_dashboard'),
]
