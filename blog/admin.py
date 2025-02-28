from django.contrib import admin
from .models import Article, ArticleCategory

# Register your models here.

class ArticleLine(admin.TabularInline):
    model = Article


class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = [ArticleLine]


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "created_on", "updated_on") 
    list_filter = ("category", "created_on")


admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(Article, ArticleAdmin)
