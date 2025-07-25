# institute/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import StudentProfile, TeacherProfile, InstituteProfile
from accounts.forms import StudentCreationForm, TeacherCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from accounts.utils import institute_required

@login_required
def institute_dashboard(request):
    institute = request.user.instituteprofile  # adjust this line based on your model
    return render(request, 'institute/institute_dashboard.html', {'institute': institute})

@institute_required
@login_required
def create_student(request):
    if request.method == 'POST':
        form = StudentCreationForm(request.POST)
        if form.is_valid():
            institute = InstituteProfile.objects.get(user=request.user)
            user = User.objects.create(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=make_password(form.cleaned_data['password']),
            )
            institute_profile = InstituteProfile.objects.get(user=request.user)
            StudentProfile.objects.create(user=user, institute=institute_profile)
            messages.success(request, 'Student created successfully!')
            return redirect('institute_dashboard')
    else:
        form = StudentCreationForm()
    return render(request, 'institute/create_student.html', {'form': form})

@institute_required
@login_required
def create_teacher(request):
    if request.method == 'POST':
        form = TeacherCreationForm(request.POST)
        if form.is_valid():
            institute = InstituteProfile.objects.get(user=request.user)
            user = User.objects.create(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=make_password(form.cleaned_data['password']),
            )
            institute_profile = InstituteProfile.objects.get(user=request.user)
            is_private = form.cleaned_data.get('is_private', False)
            TeacherProfile.objects.create(user=user, institute=institute_profile, is_private=is_private)
            messages.success(request, 'Teacher created successfully!')
            return redirect('institute_dashboard')
    else:
        form = TeacherCreationForm()
    return render(request, 'institute/create_teacher.html', {'form': form})

