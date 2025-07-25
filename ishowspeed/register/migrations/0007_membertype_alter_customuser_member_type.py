# Generated by Django 5.2.1 on 2025-05-24 08:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0006_customuser_member_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('old_viewer', 'Old Viewer'), ('subscriber', 'Subscriber'), ('fan', 'Fan'), ('lover', 'Lover'), ('cr7_fan', 'CR7 Fan')], max_length=20, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='customuser',
            name='member_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='register.membertype'),
        ),
    ]
