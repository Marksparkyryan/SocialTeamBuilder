from django import forms
from django.forms import modelformset_factory

from markdownx.widgets import MarkdownxWidget
from markdownx.fields import MarkdownxFormField
from django_select2.forms import ModelSelect2Widget

from accounts.models import Skill
from .models import Project, Position, Application

from django.utils import timezone


class SearchBarForm(forms.Form):
    """Form for searching all projects and related models (skills,
    positions)
    """
    q = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search projects...',
                'style': 'margin-bottom:0',
                'class': 'search-bar'
            },
        ))


class CreateProjectForm(forms.ModelForm):
    """Form for creating a project
    """
    STATUS = [
        ('A', 'Open'),
        ('B', 'Closed'),
        ('C', 'Complete'),
    ]

    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'class': 'card-input',
                'placeholder': 'Project Title'
            }))

    description = forms.CharField(
        widget=MarkdownxWidget(
            attrs={
                'class': 'card-input',
                'placeholder': 'Project description'
            }))

    status = forms.CharField(
        widget=forms.RadioSelect(
            choices=STATUS,
            attrs={
                'class': 'status-list'
        }))

    time_estimate = forms.CharField(
        max_length=10,
        widget=forms.TextInput(
            attrs={
                'class': 'card-input',
                'placeholder': 'Time estimate'}
        ))

    applicant_requirements = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'card-input'
            }
        )
    )

    class Meta:
        model = Project
        fields = ['title', 'description', 'time_estimate',
                  'applicant_requirements', 'status', ]


class PositionForm(forms.ModelForm):
    """Form representing a position. This form is inserted into
    PositionFormset
    """
    description = forms.CharField(
        label='',
        widget=MarkdownxWidget(
            attrs={
                'placeholder': 'Position Description',
                'class': 'card-input'
            })
    )

    time_estimate = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'card-input'
        }))

    class Meta:
        model = Position
        fields = ['title', 'description', 'skills', 'time_estimate', 'id', ]
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Position Title',
                'class': 'card-input'
            }),
            'id': forms.HiddenInput(),
        }


PositionFormset = modelformset_factory(
    Position,
    form=PositionForm,
    can_delete=True,
    max_num=10,
    extra=1,
    can_order=True
)


# Review if this really needed
class ApplicationForm(forms.ModelForm):
    created = forms.HiddenInput()

    class Meta:
        model = Application
        fields = ['user', 'position', 'status', 'unread']
    
