from django.urls import path
from . import views

app_name = 'adminpanel'  # Add this line

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('students/', views.manage_students, name='manage_students'),
    path('teachers/', views.manage_teachers, name='manage_teachers'),
    path('institutes/', views.manage_institutes, name='manage_institutes'),
    path('create-institute/', views.create_institute, name='create_institute'),
    path('logout/', views.custom_admin_logout, name='admin_logout'),
]
