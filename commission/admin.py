from django.contrib import admin
from .models import Commission, Comment


class CommentInLine(admin.TabularInline):
    model = Comment
    readonly_fields = ("created_on", "updated_on")


class CommissionAdmin(admin.ModelAdmin):
    list_display = ("title", "people_required", "created_on", "updated_on")
    search_fields = ("title", "description")
    list_filter = ("created_on", "updated_on")
    ordering = ("created_on",)
    inlines = [CommentInLine]


class CommentAdmin(admin.ModelAdmin):
    list_display = ("commission", "entry", "created_on", "updated_on")
    search_fields = ("title", "description")
    list_filter = ("created_on", "updated_on")
    ordering = ("-created_on",)


admin.site.register(Commission, CommissionAdmin)
admin.site.register(Comment, CommentAdmin)
