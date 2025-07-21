from django.urls import path
from . import views

app_name = 'adminpanel'  # Add this line

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-students/', views.manage_students, name='manage_students'),
    path('manage-teachers/', views.manage_teachers, name='manage_teachers'),
    path('manage-institutes/', views.manage_institutes, name='manage_institutes'),
    path('create-institute/', views.create_institute, name='create_institute'),
    path('logout/', views.custom_admin_logout, name='admin_logout'),
]
