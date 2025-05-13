from django.contrib import admin
from .models import Commission, Job, JobApplication


class CommissionAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "get_author_display_name",
        "get_author_username",
        "status",
        "created_on",
        "updated_on",
    )
    list_filter = ("status", "created_on")
    search_fields = (
        "title",
        "description",
        "author__display_name",
        "author__user__username",
    )
    ordering = ("created_on",)

    def get_author_display_name(self, obj):
        return obj.author.display_name

    get_author_display_name.short_description = "Author Name"

    def get_author_username(self, obj):
        return obj.author.user.username

    get_author_username.short_description = "Author Username"


class JobAdmin(admin.ModelAdmin):
    list_display = ("role", "commission", "status", "manpower_required")
    list_filter = ("status", "commission")
    search_fields = ("role", "commission__title")
    ordering = ("status", "-manpower_required", "role")


class JobApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "job",
        "get_applicant_display_name",
        "get_applicant_username",
        "status",
        "applied_on",
    )
    list_filter = ("status", "applied_on")
    search_fields = (
        "job__role",
        "applicant__display_name",
        "applicant__user__username",
    )
    ordering = ("status", "-applied_on")

    def get_applicant_display_name(self, obj):
        return obj.applicant.display_name

    get_applicant_display_name.short_description = "Applicant Name"

    def get_applicant_username(self, obj):
        return obj.applicant.user.username

    get_applicant_username.short_description = "Applicant Username"


admin.site.register(Commission, CommissionAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)
