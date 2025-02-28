from django.contrib import admin
from .models import Commission, Comment

class CommentInLine(admin.TabularInline):
    model = Comment
    readonly_fields = ('date_created_on', 'date_updated_on')

class CommissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'people_req', 'date_created_on', 'date_updated_on')
    search_fields = ('title', 'description')
    list_filter = ('date_created_on', 'date_updated_on')
    ordering = ('date_created_on',)
    inlines = [CommentInLine]

class CommentAdmin(admin.ModelAdmin):
    list_display = ('commission', 'entry', 'date_created_on', 'date_updated_on')
    search_fields =('title', 'description')
    list_filter = ('date_created_on', 'date_updated_on')
    ordering = ('-date_created_on',)


admin.site.register(Commission, CommissionAdmin)
admin.site.register(Comment, CommentAdmin)
# Register your models here.
