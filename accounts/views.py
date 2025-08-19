from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, update_session_auth_hash, logout, get_backends
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .utils import institute_required, teacher_required, student_required, admin_required
from .forms import StudentSignupForm, TeacherSignupForm, StudentProfileUpdateForm, TeacherProfileUpdateForm, InstituteProfileForm
from .models import StudentProfile, TeacherProfile, InstituteProfile, CustomUser

User = get_user_model()


def home(request):
    return render(request, 'home.html')


def student_signup(request):
    if request.method == 'POST':
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Set backend explicitly
            backend = get_backends()[0]  # Or the one you use, see note below
            user.backend = f"{backend.__module__}.{backend.__class__.__name__}"

            login(request, user)
            return redirect('dashboard')
    else:
        form = StudentSignupForm()
    return render(request, 'accounts/student_signup.html', {'form': form})


def teacher_signup(request):
    if request.method == 'POST':
        form = TeacherSignupForm(request.POST)
        if form.is_valid():
            user = form.save()

            backend = get_backends()[0]
            user.backend = f"{backend.__module__}.{backend.__class__.__name__}"

            login(request, user)
            return redirect('dashboard')
    else:
        form = TeacherSignupForm()
    return render(request, 'accounts/teacher_signup.html', {'form': form})


@login_required
def profile_view(request):
    return redirect('dashboard')


@never_cache
@login_required
def institute_profile(request):
    if request.user.role != 'institute':
        return redirect('dashboard')

    profile = request.user.instituteprofile
    return render(request, 'institute/institute_profile.html', {'profile': profile})

@never_cache
@institute_required
def institute_dashboard(request):
    profile = request.user.instituteprofile
    students = profile.studentprofile_set.all()
    teachers = profile.teacherprofile_set.all()
    return render(request, 'institute/institute_dashboard.html', {'profile': profile, 'students': students, 'teachers': teachers})

@student_required
def student_dashboard(request):
    return render(request, 'accounts/student_dashboard.html')

@teacher_required
def teacher_dashboard(request):
    return render(request, 'accounts/teacher_dashboard.html')

@never_cache
@admin_required
def admin_dashboard(request):
    context = {
        'total_students': CustomUser.objects.filter(role='student').count(),
        'total_teachers': CustomUser.objects.filter(role='teacher').count(),
        'total_institutes': InstituteProfile.objects.count(),
        'private_students': StudentProfile.objects.filter(is_private=True).count(),
        'public_students': StudentProfile.objects.filter(is_private=False).count(),
    }
    return render(request, 'adminpanel/dashboard.html', context)

@login_required
def dashboard(request):
    # Redirect based on role
    if request.user.role == 'institute':
        return redirect('institute_dashboard')
    elif request.user.role == 'student':
        return redirect('student_dashboard')
    elif request.user.role == 'teacher':
        return redirect('teacher_dashboard')
    elif request.user.is_superuser:
        return redirect('admin_dashboard')
    else:
        messages.warning(request, "No dashboard found for your role.")
        return render(request, 'accounts/dashboard.html')

@login_required
def institute_profile(request):
    profile = request.user.instituteprofile
    return render(request, 'accounts/institute_profile.html', {'profile': profile})

@login_required
def edit_institute_profile(request):
    profile = request.user.instituteprofile
    if request.method == 'POST':
        form = InstituteProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('institute_profile')
    else:
        form = InstituteProfileForm(instance=profile)
    return render(request, 'accounts/edit_institute_profile.html', {'form': form})

@never_cache
@login_required
def student_profile_view(request):
    if request.user.role != 'student':
        return redirect('dashboard')

    profile = get_object_or_404(StudentProfile, user=request.user)

    if request.method == 'POST':
        profile.bio = request.POST.get('bio', profile.bio)
        profile.date_of_birth = request.POST.get('date_of_birth', profile.date_of_birth)

    return render(request, 'accounts/student_profile.html', {
        'profile': profile
    })   



@login_required
@never_cache
def student_profile_edit(request):
    if request.user.role != 'student':
        return redirect('dashboard')

    student_profile = request.user.studentprofile

    if request.method == 'POST':
        form = StudentProfileUpdateForm(request.POST, instance=student_profile, user=request.user)
        password_form = PasswordChangeForm(user=request.user, data=request.POST)

        if form.is_valid() and password_form.is_valid():
            form.save()
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Profile and password updated successfully.")
            return redirect('student_profile')
    else:
        form = StudentProfileUpdateForm(instance=student_profile, user=request.user)
        password_form = PasswordChangeForm(user=request.user)

    return render(request, 'accounts/student_profile_edit.html', {
        'form': form,
        'password_form': password_form
    })

@never_cache
@login_required
def student_profile(request):
    student = request.user.studentprofile
    if request.method == 'POST':
        form = StudentProfileUpdateForm(request.POST, instance=student, user=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid() and password_form.is_valid():
            form.save()
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            messages.success(request, "Profile updated successfully.")
            return redirect('student_profile')
    else:
        form = StudentProfileUpdateForm(instance=student, user=request.user)
        password_form = PasswordChangeForm(request.user)

    return render(request, 'accounts/student_profile.html', {
        'form': form,
        'password_form': password_form
    })

@never_cache
@login_required
def teacher_profile(request):
    teacher = request.user.teacherprofile
    if request.method == 'POST':
        form = TeacherProfileUpdateForm(request.POST, instance=teacher, user=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid() and password_form.is_valid():
            form.save()
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            messages.success(request, "Profile updated successfully.")
            return redirect('teacher_profile')
    else:
        form = TeacherProfileUpdateForm(instance=teacher, user=request.user)
        password_form = PasswordChangeForm(request.user)

    return render(request, 'accounts/teacher_profile.html', {
        'form': form,
        'password_form': password_form
    })

@login_required
@never_cache
def edit_teacher_profile(request):
    if request.user.role != 'teacher':
        return redirect('dashboard')

    teacher_profile = request.user.teacherprofile

    if request.method == 'POST':
        form = TeacherProfileUpdateForm(request.POST, instance=teacher_profile, user=request.user)
        password_form = PasswordChangeForm(user=request.user, data=request.POST)

        if form.is_valid() and password_form.is_valid():
            form.save()
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Profile and password updated successfully.")
            return redirect('teacher_profile')
    else:
        form = TeacherProfileUpdateForm(instance=teacher_profile, user=request.user)
        password_form = PasswordChangeForm(user=request.user)

    return render(request, 'accounts/teacher_profile_edit.html', {
        'form': form,
        'password_form': password_form
    })


class StudentPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('student_profile')

    def form_valid(self, form):
        messages.success(self.request, "Password was changed successfully.")
        return super().form_valid(form)


class TeacherPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('teacher_profile')

    def form_valid(self, form):
        messages.success(self.request, "Password was changed successfully.")
        return super().form_valid(form)
    

@staff_member_required
@admin_required
def admin_dashboard(request):
    context = {
        'total_students': CustomUser.objects.filter(role='student').count(),
        'total_teachers': CustomUser.objects.filter(role='teacher').count(),
        'total_institutes': InstituteProfile.objects.count(),
        'private_students': StudentProfile.objects.filter(is_private=True).count(),
        'public_students': StudentProfile.objects.filter(is_private=False).count(),
    }
    return render(request, 'adminpanel/dashboard.html', context)

def secure_logout(request):
    # Optional: clear all sessions for the current user
    if request.user.is_authenticated:
        user_sessions = Session.objects.filter(expire_date__gte=timezone.now())
        for session in user_sessions:
            data = session.get_decoded()
            if data.get('_auth_user_id') == str(request.user.id):
                session.delete()

    logout(request)
    return redirect('login')
