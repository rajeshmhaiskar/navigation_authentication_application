# Generated by Django 4.2 on 2024-01-24 08:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('GenesysUserApp', '0001_initial'),
        ('GenesysAuthenticator', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='schemaaccess',
            name='database',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GenesysUserApp.masterdatabase'),
        ),
        migrations.AddField(
            model_name='schemaaccess',
            name='schema',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GenesysAuthenticator.masterdatabaseschema'),
        ),
        migrations.AddField(
            model_name='schemaaccess',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='privilegefunctionvalidation',
            name='database',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GenesysUserApp.masterdatabase'),
        ),
        migrations.AddField(
            model_name='privilegefunctionvalidation',
            name='granted_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='granted_privileges', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='privilegefunctionvalidation',
            name='schema',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GenesysAuthenticator.masterdatabaseschema'),
        ),
        migrations.AddField(
            model_name='privilegefunctionvalidation',
            name='table',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='GenesysAuthenticator.databasetable'),
        ),
        migrations.AddField(
            model_name='masterdatabaseschema',
            name='database',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GenesysUserApp.masterdatabase'),
        ),
        migrations.AddField(
            model_name='databasetable',
            name='database',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GenesysUserApp.masterdatabase'),
        ),
        migrations.AddField(
            model_name='databasetable',
            name='schema',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GenesysAuthenticator.masterdatabaseschema'),
        ),
        migrations.AddField(
            model_name='databasepermission',
            name='database',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GenesysUserApp.masterdatabase'),
        ),
        migrations.AddField(
            model_name='databasepermission',
            name='granted_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='permissions_given', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='databasepermission',
            name='schemas',
            field=models.ManyToManyField(to='GenesysAuthenticator.masterdatabaseschema'),
        ),
        migrations.AddField(
            model_name='databasepermission',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='databaseaccess',
            name='databases',
            field=models.ManyToManyField(to='GenesysUserApp.masterdatabase'),
        ),
        migrations.AddField(
            model_name='databaseaccess',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='database_access', to=settings.AUTH_USER_MODEL),
        ),
    ]
