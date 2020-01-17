from django import forms
from django.conf import settings
from django.forms import formset_factory, modelformset_factory
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from accounts.models import PortfolioProject, Skill, User

from django_select2.forms import Select2TagWidget, ModelSelect2TagWidget
from select2_tags import forms as f


# Admin Form
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

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
            print(user._meta.default_manager_name)
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


class UserUpdateForm(f.Select2ModelForm):
    skills = f.Select2ModelMultipleChoiceField(
        'name', queryset=Skill.objects.all(), required=False, save_new=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'about', 'avatar', 'skills']
             

class PortfolioProjectForm(forms.ModelForm):
    class Meta:
        model = PortfolioProject
        fields = ['name', 'url']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Project Name'}),
            'url': forms.TextInput(attrs={'placeholder': 'Project URL'}),
        }

    
# PortfolioProjectFormset = formset_factory(PortfolioProjectForm, extra=0)
NewPortfolioProjectFormset = modelformset_factory(
    PortfolioProject,
    form=PortfolioProjectForm,
    can_delete=True,
    max_num=5,
    extra=0,
    can_order=True
    )
