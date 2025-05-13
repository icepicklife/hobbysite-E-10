from django import forms
from .models import Article, Comment, ArticleCategory


class ArticleForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=ArticleCategory.objects.all(), empty_label="Select a category"
    )

    class Meta:
        model = Article
        fields = ["title", "category", "entry", "header"]

class ArticleImageUploadForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["header"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["entry"]
