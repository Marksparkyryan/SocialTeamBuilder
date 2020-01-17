from django import forms
from django.forms import formset_factory, modelformset_factory

from .models import Project, Position
from accounts.models import Skill

from django_select2.forms import Select2TagWidget, ModelSelect2TagWidget
from select2_tags import forms as f


class CreateProjectForm(forms.ModelForm):
    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'class': 'circle--input--h1',
                'placeholder': 'Project Title'}
        ))
    description = forms.CharField(
        max_length=255,
        widget=forms.Textarea(
            attrs={'placeholder': 'Project description...'}))
    time_estimate = forms.CharField(
        max_length=10,
        widget=forms.TextInput(
            attrs={
                'class': 'circle--textarea--input',
                'placeholder': 'Time estimate'}
        ))

    class Meta:
        model = Project
        fields = ['title', 'description', 'time_estimate', 'applicant_requirements',]



class PositionForm(forms.ModelForm):
    skills = f.Select2ModelMultipleChoiceField(
        'name', 
        queryset=Skill.objects.all(), 
        required=False, 
        save_new=True,
    )

    class Meta:
        model = Position
        fields = ['title', 'description', 'skills', 'time_estimate']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Position Title',
                'class': 'circle--input--h3'
            }),
            'description': forms.Textarea(attrs={'placeholder': 'Position description'}),
        }        

    
# PortfolioProjectFormset = formset_factory(PortfolioProjectForm, extra=0)
PositionFormset = modelformset_factory(
    Position,
    form=PositionForm,
    can_delete=True,
    max_num=10,
    extra=1,
    can_order=True
    )
