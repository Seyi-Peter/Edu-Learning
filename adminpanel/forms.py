from django import forms
from accounts.models import InstituteProfile, CustomUser

class InstituteCreationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = InstituteProfile
        fields = ['name', 'username', 'email', 'password']  # Add other fields if needed

    def save(self, commit=True):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        name = self.cleaned_data['name']

        # Create user first
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='institute'  # Make sure this matches your role field
        )

        # Then create the institute profile
        institute = InstituteProfile(user=user, name=name)

        if commit:
            user.save()
            institute.save()

        return institute
