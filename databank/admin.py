from django.contrib import admin

# Register your models here.
from .models import Artist, Work, Status


class WorksAdmin(admin.ModelAdmin):
    list_display = ("name", "artist", "storage_tag",)
    list_filter = ("artist",)
    prepopulated_fields = {"slug": ("name",)}


class StatusAdmin(admin.ModelAdmin):
    list_display = ("work", "buyer", "date",)
    list_filter = ("buyer", "work",)


admin.site.register(Status, StatusAdmin)
admin.site.register(Artist)
admin.site.register(Work, WorksAdmin)
