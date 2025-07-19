from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    USER_ROLES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('institute', 'Institute'),
        
    

    )
    role = models.CharField(max_length=10, choices=USER_ROLES)
    is_verified = models.BooleanField(default=False)
    email = models.EmailField(unique=True) # Ensure email is unique
    

    def __str__(self):
        return f"{self.username} ({self.role})"

class InstituteProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'institute'})
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name

class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    institute = models.ForeignKey('InstituteProfile', null=True, blank=True, on_delete=models.SET_NULL)
    is_private = models.BooleanField(default=True)
    bio = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='students_profiles/', blank=True, null=True)


    def __str__(self):
        return self.user.username

class TeacherProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    institute = models.ForeignKey('InstituteProfile', null=True, blank=True, on_delete=models.SET_NULL)
    is_private = models.BooleanField(default=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
