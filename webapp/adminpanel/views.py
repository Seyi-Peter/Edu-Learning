from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from accounts.models import CustomUser, StudentProfile, TeacherProfile, InstituteProfile
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from .forms import InstituteCreationForm


@staff_member_required
def admin_dashboard(request):
    total_students = StudentProfile.objects.count()
    total_teachers = TeacherProfile.objects.count()
    total_institutes = InstituteProfile.objects.count()

    return render(request, 'adminpanel/dashboard.html', {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_institutes': total_institutes,
    })

@staff_member_required
def manage_students(request):
    students = StudentProfile.objects.select_related('user', 'institute')
    return render(request, 'adminpanel/manage_students.html', {'students': students})

@staff_member_required
def manage_teachers(request):
    teachers = TeacherProfile.objects.select_related('user', 'institute')
    return render(request, 'adminpanel/manage_teachers.html', {'teachers': teachers})

@staff_member_required
def manage_institutes(request):
    institutes = InstituteProfile.objects.all()
    return render(request, 'adminpanel/manage_institutes.html', {'institutes': institutes})

@login_required
def custom_admin_logout(request):
    logout(request)
    return redirect('login')

@staff_member_required
def create_institute(request):
    if request.method == 'POST':
        form = InstituteCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Institute account created successfully.")
            return redirect('adminpanel:manage_institutes')
    else:
        form = InstituteCreationForm()
    return render(request, 'adminpanel/create_institute.html', {'form': form})

