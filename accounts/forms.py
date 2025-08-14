from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import CustomUser, StudentProfile, TeacherProfile, InstituteProfile


# Base Tailwind widget styles
TAILWIND_INPUT = "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
TAILWIND_SELECT = "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 bg-white"
TAILWIND_CHECKBOX = "h-4 w-4 text-purple-600 border-gray-300 rounded focus:ring-purple-500"


class StudentSignupForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": TAILWIND_INPUT, "placeholder": " "})
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": TAILWIND_INPUT, "placeholder": " "})
    )
    is_private = forms.BooleanField(
        required=False,
        label="Are you registering as a private student?",
        widget=forms.CheckboxInput(attrs={"class": TAILWIND_CHECKBOX})
    )
    institute = forms.ModelChoiceField(
        queryset=InstituteProfile.objects.all(),
        required=False,
        help_text="Select institute if not a private student",
        widget=forms.Select(attrs={"class": TAILWIND_SELECT})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={"class": TAILWIND_INPUT, "placeholder": ""}),
            'email': forms.EmailInput(attrs={"class": TAILWIND_INPUT, "placeholder": ""}),
            'password1': forms.PasswordInput(attrs={"class": TAILWIND_INPUT, "placeholder": ""}),
            'password2': forms.PasswordInput(attrs={"class": TAILWIND_INPUT, "placeholder": " "}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'student'
        if commit:
            user.save()
            StudentProfile.objects.create(
                user=user,
                is_private=self.cleaned_data.get('is_private'),
                institute=self.cleaned_data.get('institute') if not self.cleaned_data.get('is_private') else None
            )
        return user


class TeacherSignupForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={"class": TAILWIND_INPUT, "placeholder": " "})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={"class": TAILWIND_INPUT, "placeholder": " "})
    )
    is_private = forms.BooleanField(
        required=False,
        label="Are you registering as a private teacher?",
        widget=forms.CheckboxInput(attrs={"class": TAILWIND_CHECKBOX})
    )
    institute = forms.ModelChoiceField(
        queryset=InstituteProfile.objects.all(),
        required=False,
        help_text="Select your institute (leave blank if private)",
        widget=forms.Select(attrs={"class": TAILWIND_SELECT})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={"class": TAILWIND_INPUT, "placeholder": ""}),
            'email': forms.EmailInput(attrs={"class": TAILWIND_INPUT, "placeholder": ""}),
            'password1': forms.PasswordInput(attrs={"class": TAILWIND_INPUT, "placeholder": ""}),
            'password2': forms.PasswordInput(attrs={"class": TAILWIND_INPUT, "placeholder": ""}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'teacher'
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            TeacherProfile.objects.create(
                user=user,
                is_private=self.cleaned_data['is_private'],
                institute=self.cleaned_data['institute'] if not self.cleaned_data['is_private'] else None
            )
        return user
    
    
class StudentProfileUpdateForm(forms.ModelForm):
    username = UsernameField(
        label="Username",
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = StudentProfile
        fields = ['bio']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['username'].initial = user.username

    def save(self, commit=True):
        profile = super().save(commit=False)
        self.user.username = self.cleaned_data['username']
        if commit:
            self.user.save()
            profile.save()
        return profile
    
 
class TeacherProfileUpdateForm(forms.ModelForm):
    username = UsernameField(
        label="Username",
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = TeacherProfile
        fields = ['bio']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['username'].initial = user.username

    def save(self, commit=True):
        profile = super().save(commit=False)
        self.user.username = self.cleaned_data['username']
        if commit:
            self.user.save()
            profile.save()
        return profile   

class InstituteProfileForm(forms.ModelForm):
    class Meta:
        model = InstituteProfile
        fields = ['name', 'address']


class StudentCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'student'
        if commit:
            user.save()
            StudentProfile.objects.create(user=user)
        return user


class TeacherCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'teacher'
        if commit:
            user.save()
            TeacherProfile.objects.create(user=user)
        return user