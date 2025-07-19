from django.contrib import admin
from accounts.models import CustomUser, StudentProfile, TeacherProfile, InstituteProfile
from accounts.admin import CustomUserAdmin  # reuse the existing custom admin

# Avoid AlreadyRegistered error
from django.contrib.admin.sites import AlreadyRegistered

try:
    admin.site.register(CustomUser, CustomUserAdmin)
except AlreadyRegistered:
    pass

for model in [StudentProfile, TeacherProfile, InstituteProfile]:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass
# This code registers the models with the admin site, ensuring that
# the custom user admin is used for CustomUser and avoids duplicate registration errors.