from django.contrib import admin
from .models import Thread, ThreadCategory, Comment


class ThreadInline(admin.TabularInline):
    model = Thread
    extra = 1


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    readonly_fields = ("created_on", "updated_on")


class ThreadCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
    inlines = [ThreadInline]


class ThreadAdmin(admin.ModelAdmin):
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
    list_display = ("thread_title", "author_display_name", "created_on")
    list_filter = ("created_on", "thread")
    search_fields = ("entry", "author__display_name", "thread__title")
    date_hierarchy = "created_on"
    ordering = ("created_on",)
    readonly_fields = ("created_on", "updated_on")

    def thread_title(self, obj):
        return obj.thread.title

    thread_title.short_description = "Thread"

    def author_display_name(self, obj):
        if obj.author:
            return obj.author.display_name
        return None

    author_display_name.short_description = "Author"


admin.site.register(ThreadCategory, ThreadCategoryAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Comment, CommentAdmin)
