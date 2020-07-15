from django import forms
from django.forms import modelformset_factory
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm

from markdownx.fields import MarkdownxFormField
from markdownx.widgets import MarkdownxWidget

from accounts.models import PortfolioProject, Skill


User = get_user_model()

class MyAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Email',
                'class': 'card-input'
                })
    )
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'class': 'card-input'
                })
    )

    class Meta:
        model = User

# Admin Form
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email Address',
                'class': 'card-input'
                })
    )
    first_name = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'First Name',
                'class': 'card-input'
                })
    )
    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'class': 'card-input'
                })
    )
    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Password',
            'class': 'card-input'
            })
    )

    class Meta:
        model = User
        fields = ('email', 'first_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# Admin Form
class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


class UserUpdateForm(forms.ModelForm):
    """Form for updating user's general information (first_name,
    last_name, about, avatar, skills)
    """
    about = forms.CharField(
        widget=MarkdownxWidget(
            attrs={
                "class": "card-input",
                "placeholder": "Add a short description about yourself..."
            }))

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "card-input",
                "placeholder": "First Name"
            }))

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "card-input",
                "placeholder": "Last Name"
            }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'about', 'skills']


class AvatarForm(forms.ModelForm):
    """Form holding the user's avatar. We're using a separate form so
    cropperjs can update outside of the other user data
    """
    class Meta:
        model = User
        fields = [
            'avatar',
        ]

    class Media:
        css = {'all': ('cropperjs/dist/cropper.css',)}
        js = ('cropperjs/dist/cropper.js',
              'jquery-cropper/dist/jquery-cropper.js',
              )


class PortfolioProjectForm(forms.ModelForm):
    """Form for updating portfolio projects related toa specific user -
    (name, url)
    """
    class Meta:
        model = PortfolioProject
        fields = ['name', 'url', 'id', ]
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Project Name',
                'class': 'card-input'
                }),
            'url': forms.TextInput(attrs={
                'placeholder': 'Project URL',
                'class': 'card-input'
                }),
            'id': forms.HiddenInput()
        }


NewPortfolioProjectFormset = modelformset_factory(
    PortfolioProject,
    form=PortfolioProjectForm,
    can_delete=True,
    max_num=10,
    extra=1,
    can_order=True
)
