from django.db import models
import jsonfield
from GenesysUserApp.models import *


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class MasterDatabaseSchema(BaseModel):
    database = models.ForeignKey(MasterDatabase, on_delete=models.CASCADE, null=False, blank=False)
    schema = models.CharField(max_length=255, null=False, blank=False)
    is_active = models.BooleanField(null=False, blank=False)

    def __str__(self):
        return self.schema

    class Meta:
        verbose_name = "Database Schema"
        verbose_name_plural = "Database Schemas"


class DatabaseAccess(BaseModel):
    user = models.OneToOneField(UserDetails, on_delete=models.CASCADE, related_name='database_access', null=False,
                                blank=False)
    databases = models.ManyToManyField(MasterDatabase)

    def __str__(self):
        # Assuming MasterDatabase has a 'database_name' field
        databases_str = ', '.join(
            [db.database_name for db in self.databases.all()]) if self.databases.exists() else 'None'
        return f"{self.user.emp_id} - Databases: {databases_str}"


class DatabasePermission(BaseModel):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, null=False, blank=False)
    database = models.ForeignKey(MasterDatabase, on_delete=models.CASCADE, null=False, blank=False)
    granted_by = models.ForeignKey(UserDetails, on_delete=models.SET_NULL, related_name='permissions_given', null=True,
                                   blank=True)
    schemas = models.ManyToManyField(MasterDatabaseSchema)
    db_access = models.BooleanField(default=False)
    privilege_select = models.BooleanField(default=False)
    privilege_insert = models.BooleanField(default=False)
    privilege_update = models.BooleanField(default=False)
    privilege_delete = models.BooleanField(default=False)
    privilege_sequence = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.emp_id}"


class SchemaAccess(BaseModel):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, null=False, blank=False)
    database = models.ForeignKey(MasterDatabase, on_delete=models.CASCADE, null=False, blank=False)
    schema = models.ForeignKey(MasterDatabaseSchema, on_delete=models.CASCADE, null=False, blank=False)
    has_access = models.BooleanField(default=False)


class DatabaseTable(models.Model):
    database = models.ForeignKey(MasterDatabase, on_delete=models.CASCADE, null=False, blank=False)
    schema = models.ForeignKey(MasterDatabaseSchema, on_delete=models.CASCADE, null=False, blank=False)
    table_name = models.CharField(max_length=255, null=False, blank=False)
    columns = jsonfield.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.database.database_name} - {self.schema.schema} - {self.table_name}"


class PrivilegeFunctionValidation(BaseModel):
    granted_by = models.ForeignKey(UserDetails, on_delete=models.SET_NULL, related_name='granted_privileges', null=True,
                                   blank=True)
    database = models.ForeignKey(MasterDatabase, on_delete=models.CASCADE, null=False, blank=False)
    schema = models.ForeignKey(MasterDatabaseSchema, on_delete=models.CASCADE, null=False, blank=False)
    table = models.ForeignKey(DatabaseTable, on_delete=models.CASCADE, null=True, blank=True)
    columns = models.CharField(max_length=255, unique=True, null=False, blank=False)
    privilege_function_validation = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.database.database_name} - {self.schema.schema} - {self.table.table_name}"
