from django.contrib import admin
from .models import UserDetails, MasterDatabase


class MasterDatabaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'database_name', 'server_ip', 'port', 'username', 'is_active')
    search_fields = ('database_name', 'server_ip', 'username')


admin.site.register(MasterDatabase, MasterDatabaseAdmin)


class UserDetailsAdmin(admin.ModelAdmin):
    list_display = (
        'emp_id', 'email', 'designation', 'is_active', 'has_resigned', 'display_selected_databases'
    )
    search_fields = ('emp_id', 'email')
    list_filter = ('designation', 'is_active', 'has_resigned')
    filter_horizontal = ('selected_databases',)

    def display_selected_databases(self, obj):
        return ", ".join([db.database_name for db in obj.selected_databases.all()])

    display_selected_databases.short_description = 'Selected Databases'


admin.site.register(UserDetails, UserDetailsAdmin)
