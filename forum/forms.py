from django import forms
from .models import Thread, Comment, ThreadCategory

class ThreadForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=ThreadCategory.objects.all(), empty_label="Select a category")
    class Meta:
        model = Thread
        fields = ['title', 'category', 'entry', 'image']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['entry']