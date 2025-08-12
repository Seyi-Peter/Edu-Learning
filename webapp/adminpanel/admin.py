from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import CustomUser, StudentProfile, TeacherProfile, InstituteProfile

# Custom user admin class
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'is_staff']
    list_filter = ['role', 'is_staff', 'is_superuser']

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Role', {'fields': ('role',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'username')
    ordering = ('username',)

# Register all models here
models = [
    (CustomUser, CustomUserAdmin),
    (StudentProfile, None),
    (TeacherProfile, None),
    (InstituteProfile, None),
]

for model, admin_class in models:
    try:
        admin.site.register(model, admin_class) if admin_class else admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
