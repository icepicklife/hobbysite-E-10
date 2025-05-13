from django.contrib import admin
from .models import Article, ArticleCategory, Comment


class ArticleInline(admin.TabularInline):
    model = Article
    extra = 1


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    readonly_fields = ("created_on", "updated_on")


class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
    inlines = [ArticleInline]


class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author_display_name",
        "category",
        "created_on",
        "updated_on",
    )
    list_filter = ("category", "created_on")
    search_fields = ("title", "entry")
    date_hierarchy = "created_on"
    ordering = ("created_on",)
    readonly_fields = ("created_on", "updated_on")

    def author_display_name(self, obj):
        if obj.author:
            return obj.author.display_name
        return None

    author_display_name.short_description = "Author"

    inlines = [CommentInline]


class CommentAdmin(admin.ModelAdmin):
    list_display = ("article_title", "author_display_name", "created_on")
    list_filter = ("created_on", "article")
    search_fields = ("entry", "author__display_name", "article__title")
    date_hierarchy = "created_on"
    ordering = ("created_on",)
    readonly_fields = ("created_on", "updated_on")

    def article_title(self, obj):
        return obj.article.title

    article_title.short_description = "Article"

    def author_display_name(self, obj):
        if obj.author:
            return obj.author.display_name
        return None

    author_display_name.short_description = "Author"


admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
