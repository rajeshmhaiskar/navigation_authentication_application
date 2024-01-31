from django import forms
from .models import DatabasePermission, MasterDatabase, MasterDatabaseSchema, DatabaseTable, PrivilegeFunctionValidation
from GenesysUserApp.models import *
from GenesysUserApp.constants import TABLE_ALIAS_LIST


class GrantPermissionForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=UserDetails.objects.all(), required=True)
    database = forms.ModelChoiceField(queryset=MasterDatabase.objects.all(), required=True)
    schema = forms.ModelChoiceField(queryset=MasterDatabaseSchema.objects.all(), required=False)
    table_alias = forms.ChoiceField(choices=TABLE_ALIAS_LIST, required=True)

    class Meta:
        model = DatabasePermission
        fields = ['user', 'database', 'schema', 'table_alias', 'db_access', 'privilege_select',
                  'privilege_insert', 'privilege_update', 'privilege_delete',
                  'privilege_sequence']

    def __init__(self, *args, **kwargs):
        super(GrantPermissionForm, self).__init__(*args, **kwargs)


class PrivilegeFunctionValidationForm(forms.ModelForm):
    class Meta:
        model = PrivilegeFunctionValidation
        fields = ['database', 'schema', 'table', 'columns', 'privilege_function_validation']

    columns = forms.CharField(max_length=255, required=False, widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set initial choices for the dropdowns (subject to change dynamically)
        self.fields['database'].queryset = MasterDatabase.objects.filter(is_active=True)
        self.fields['schema'].queryset = MasterDatabaseSchema.objects.filter(is_active=True)
        self.fields['table'].queryset = DatabaseTable.objects.all()
        self.fields['columns'].queryset = []  # Initial empty queryset for columns

        # Add JavaScript event attributes to trigger AJAX requests
        self.fields['database'].widget.attrs['onchange'] = 'load_schemas()'
        self.fields['schema'].widget.attrs['onchange'] = 'load_tables()'
        self.fields['table'].widget.attrs['onchange'] = 'load_columns()'
