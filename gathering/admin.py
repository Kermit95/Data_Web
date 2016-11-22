from django.contrib import admin
from gathering.models import DataTable, UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    pass

class DataTableAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(DataTable, DataTableAdmin)
