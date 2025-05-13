from django import forms
from .models import Article, Comment, ArticleCategory


class ArticleImageUploadForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["header_image"]


class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ["created_on", "updated_on", "author"]


class ArticleCategoryCreateForm(forms.ModelForm):
    class Meta:
        model = ArticleCategory
        fields = ["name", "description"]


class ArticleUpdateForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ["created_on", "author"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ["created_on", "updated_on", "author", "article"]
