from django import forms
from accounts.models import CustomUser, InstituteProfile

class InstituteCreationForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    name = forms.CharField()
    address = forms.CharField()

    class Meta:
        model = CustomUser
        fields = ['email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.role = 'institute'
        if commit:
            user.save()
            InstituteProfile.objects.create(
                user=user,
                name=self.cleaned_data['name'],
                address=self.cleaned_data['address']
            )
        return user
