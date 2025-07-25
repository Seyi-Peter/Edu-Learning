from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect

def institute_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'institute':
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Access Denied: Institute access only.')
        return redirect('login')
    return wrapper

def teacher_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'teacher':
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Access Denied: Teacher access only.')
        return redirect('login')
    return wrapper

def student_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'student':
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Access Denied: Student access only.')
        return redirect('login')
    return wrapper

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Access Denied: Admin access only.')
        return redirect('login')
    return wrapper
