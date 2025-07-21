from django import forms
from accounts.models import CustomUser, InstituteProfile

class InstituteCreationForm(forms.Form):
    email = forms.EmailField(label="Official Email")
    password = forms.CharField(widget=forms.PasswordInput)
    name = forms.CharField(label="Institute Name")
    address = forms.CharField(label="Institute Address")

    def save(self, commit=True):
        # Create user
        user = CustomUser(
            email=self.cleaned_data['email'],
            role='institute'
        )
        user.set_password(self.cleaned_data['password'])
        
        # Validate email uniqueness
        def clean_email(self):
            email = self.cleaned_data['email']
            if CustomUser.objects.filter(email=email).exists():
                raise forms.ValidationError("A user with this email already exists.")
            return email
        # Save user if commit is True
        if commit:
            user.save()
            InstituteProfile.objects.create(
                user=user,
                name=self.cleaned_data['name'],
                address=self.cleaned_data['address']
            )
        return user
    
