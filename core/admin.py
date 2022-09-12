from django.contrib import admin
from .models import Photo
# Register your models here.


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title','created')
    list_filter = ('created',)
    search_fields = ('title',)
    prepopulated_fields = {'slug':('title',)}
admin.site.register(Photo,PhotoAdmin)
#admin.site.register(ViewedPhoto)