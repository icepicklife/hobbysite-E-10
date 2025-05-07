from django import forms
from .models import Article, Comment

class ArticleImageUploadForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["header_image"]

class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ["created_on", "updated_on", "author"]

class ArticleUpdateForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ["created_on", "author"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ["created_on", "updated_on", "author", "article"]