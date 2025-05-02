from django import forms
from django.forms import inlineformset_factory
from .models import Commission, Job, JobApplication


class CommissionForm(forms.ModelForm):

    class Meta:

        model = Commission
        exclude = ['author', 'created_on', 'updated_on']


class JobForm(forms.ModelForm):

    class Meta:

        model = Job
        fields = ['role', 'manpower_required', 'status']

JobFormSet = inlineformset_factory(
    Commission,
    Job,
    fields=('role', 'manpower_required', 'status'),
    extra=1,
    can_delete=False
)


class JobApplicationForm(forms.ModelForm):

    class Meta:
        
        model = JobApplication
        exclude = ['applicant', 'applied_on']