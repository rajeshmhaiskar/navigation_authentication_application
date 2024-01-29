from django.contrib import admin
from .models import MasterDatabase, MasterDatabaseSchema, DatabaseAccess, DatabasePermission, SchemaAccess, \
    DatabaseTable, PrivilegeFunctionValidation


class MasterDatabaseSchemaAdmin(admin.ModelAdmin):
    list_display = ('database', 'schema', 'is_active')
    search_fields = ('database__database_name', 'schema')


admin.site.register(MasterDatabaseSchema, MasterDatabaseSchemaAdmin)


class DatabaseAccessAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_databases')
    search_fields = ('user__emp_id', 'databases__database_name')

    def display_databases(self, obj):
        return ', '.join([db.database_name for db in obj.databases.all()])


admin.site.register(DatabaseAccess, DatabaseAccessAdmin)


class DatabasePermissionAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'database', 'granted_by', 'display_schema', 'table_alias', 'db_access', 'privilege_select', 'privilege_insert',
        'privilege_update', 'privilege_delete'
    )
    search_fields = ('user__emp_id', 'database__database_name')

    def display_schema(self, obj):
        return str(obj.schema) if obj.schema else ''

    display_schema.short_description = 'Schema'


admin.site.register(DatabasePermission, DatabasePermissionAdmin)


class SchemaAccessAdmin(admin.ModelAdmin):
    list_display = ('user', 'database', 'schema', 'has_access')
    search_fields = ('user__emp_id', 'database__user__emp_id', 'schema__schema')


admin.site.register(SchemaAccess, SchemaAccessAdmin)


class DatabaseTableAdmin(admin.ModelAdmin):
    list_display = ('database', 'schema', 'table_name', 'columns')


admin.site.register(DatabaseTable, DatabaseTableAdmin)


class PrivilegeFunctionValidationAdmin(admin.ModelAdmin):
    list_display = (
        'database', 'schema', 'table', 'columns', 'privilege_function_validation', 'granted_by', 'created_at',
        'updated_at')


admin.site.register(PrivilegeFunctionValidation, PrivilegeFunctionValidationAdmin)
