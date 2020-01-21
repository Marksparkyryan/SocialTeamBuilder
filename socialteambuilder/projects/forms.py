from django import forms
from django.forms import modelformset_factory

from ckeditor.widgets import CKEditorWidget
from select2_tags import forms as f

from accounts.models import Skill
from .models import Project, Position


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
    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'class': 'circle--input--h1',
                'placeholder': 'Project Title'}
        ))
    description = forms.CharField(widget=CKEditorWidget())
    time_estimate = forms.CharField(
        max_length=10,
        widget=forms.TextInput(
            attrs={
                'class': 'circle--textarea--input',
                'placeholder': 'Time estimate'}
        ))

    class Meta:
        model = Project
        fields = ['title', 'description', 'time_estimate',
                  'applicant_requirements', 'status', ]


class PositionForm(forms.ModelForm):
    """Form representing a position. This form is inserted into
    PositionFormset
    """
    skills = f.Select2ModelMultipleChoiceField(
        'name',
        queryset=Skill.objects.all(),
        required=False,
        save_new=True,
    )

    class Meta:
        model = Position
        fields = ['title', 'description', 'skills', 'time_estimate', 'id', ]
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Position Title',
                'class': 'circle--input--h3'
            }),
            'description': CKEditorWidget(),
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
