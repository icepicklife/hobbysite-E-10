from django.contrib import admin
from .models import Post, PostCategory

# Register your models here.

class PostLine(admin.TabularInline):
    model = Post


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = [PostLine]


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "created_on", "updated_on") 
    list_filter = ("category", "created_on")


admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Post, PostAdmin)
