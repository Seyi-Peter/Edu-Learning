from django.urls import path
from . import views

app_name = 'institute'

urlpatterns = [
    path('dashboard/', views.institute_dashboard, name='institute_dashboard'),
    path('create-student/', views.create_student, name='create_student'),
    path('create-teacher/', views.create_teacher, name='create_teacher'),
]
