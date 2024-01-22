# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .constants import DESIGNATION_CHOICES
from .models import DatabasePermission, UserDetails, MasterDatabase, MasterDatabaseSchema, DatabaseTable
from .models import PrivilegeFunctionValidation
from django import forms
from .models import PrivilegeFunctionValidation


class RegistrationForm(UserCreationForm):
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    selected_databases = forms.ModelMultipleChoiceField(
        queryset=MasterDatabase.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False,
        label='Select Databases'
    )

    class Meta:
        model = UserDetails
        fields = ['emp_id', 'email', 'designation', 'password1', 'password2', 'selected_databases']
        widgets = {
            'designation': forms.Select(choices=DESIGNATION_CHOICES),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

        # Save selected database names as a list of strings
        selected_databases = self.cleaned_data.get('selected_databases')
        if selected_databases:
            user.selected_databases.set(selected_databases)

        return user


class GrantPermissionForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=UserDetails.objects.all(), required=True)
    database = forms.ModelChoiceField(queryset=MasterDatabase.objects.all(), required=True)
    schemas = forms.ModelMultipleChoiceField(queryset=MasterDatabaseSchema.objects.all(), required=False)

    class Meta:
        model = DatabasePermission
        fields = ['user', 'database', 'schemas', 'db_access', 'privilege_select',
                  'privilege_insert', 'privilege_update', 'privilege_delete',
                  'privilege_sequence']

    def __init__(self, *args, **kwargs):
        super(GrantPermissionForm, self).__init__(*args, **kwargs)


class PrivilegeFunctionValidationForm(forms.ModelForm):
    class Meta:
        model = PrivilegeFunctionValidation
        fields = ['database', 'schema', 'table', 'columns', 'privilege_function_validation']
        labels = {
            'database': 'Select Database',
            'schema': 'Select Schema',
            'table': 'Select Table',
            'columns': 'Select Column',
            'privilege_function_validation': 'Enable Privilege Function Validation',
        }
        widgets = {
            'columns': forms.TextInput(attrs={'class': 'columns-input'}),  # Change to TextInput
            'privilege_function_validation': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super(PrivilegeFunctionValidationForm, self).__init__(*args, **kwargs)

        # Make the 'schema', 'table', and 'columns' fields initially empty
        self.fields['schema'].queryset = MasterDatabaseSchema.objects.none()
        self.fields['table'].queryset = DatabaseTable.objects.none()

        # Fetch the column names passed from the view and update the 'columns' field
        column_names = kwargs.get('column_names', [])
        self.fields['columns'].widget.attrs['list'] = 'column_list'