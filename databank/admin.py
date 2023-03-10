from django.contrib import admin
# Register your models here.
from .models import Artist, Work, Renter


class RenterAdmin(admin.ModelAdmin):
    list_display = ("name", "company_name")
    prepopulated_fields = {"slug": ("name",)}


class ArtistAdmin(admin.ModelAdmin):
    list_display = ("name", "storagetag", "factor",)
    prepopulated_fields = {"slug": ("name",)}


class WorksAdmin(admin.ModelAdmin):
    list_display = ("name", "artist")
    list_filter = ("artist",)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Artist, ArtistAdmin)
admin.site.register(Work, WorksAdmin)
admin.site.register(Renter, RenterAdmin)
