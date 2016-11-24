from django.contrib import admin
from gathering.models import DataTable, UserProfile, DataTableOwner, DataTableItem

class UserProfileAdmin(admin.ModelAdmin):
    pass

class DataTableAdmin(admin.ModelAdmin):
    pass

class DataTableItemAdmin(admin.ModelAdmin):
    pass

class DataTableOwnerAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(DataTable, DataTableAdmin)
admin.site.register(DataTableOwner, DataTableOwnerAdmin)
admin.site.register(DataTableItem, DataTableItemAdmin)
