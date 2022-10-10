from django import forms
from crispy_forms.helper import FormHelper

from resume.models import ResumeCourse, ResumeHeader, ResumeJob, ResumeProfessionalSummary, ResumeSkill

class ResumeHeaderForm(forms.ModelForm):

    class Meta:
        model = ResumeHeader
        fields = ['profile_picture', 'firstname', 'lastname', 'age', 'profession', 'city', 'state', 'phone', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # need to be initialized for the profile picture field
        self.helper = FormHelper()

class ResumeSummaryForm(forms.ModelForm):

    class Meta:
        model = ResumeProfessionalSummary
        fields = ['description']

class ResumeSkillForm(forms.ModelForm):

    class Meta:
        model = ResumeSkill
        fields = ['skill_summary', 'rating']

class ResumeJobForm(forms.ModelForm):

    class Meta:
        model = ResumeJob
        fields = ['occupation', 'company_name', 'entry_date', 'leave_date', 'description']
        widgets = {
            'entry_date': forms.DateInput(format=('%Y-%m-%d'), attrs={'placeholder':'Select a date', 'type':'date'}),
            'leave_date': forms.DateInput(format=('%Y-%m-%d'), attrs={'placeholder':'Select a date', 'type':'date'}),
            'description': forms.Textarea(attrs={'cols': '200'})
        }

class ResumeCourseForm(forms.ModelForm):

    class Meta:
        model = ResumeCourse
        fields = ['major', 'college_name', 'entry_date', 'leave_date', 'description']
        widgets = {
            'entry_date': forms.DateInput(format=('%Y-%m-%d'), attrs={'placeholder':'Select a date', 'type':'date'}),
            'leave_date': forms.DateInput(format=('%Y-%m-%d'), attrs={'placeholder':'Select a date', 'type':'date'}),
            'description': forms.Textarea(attrs={'cols': '200'})
        }

