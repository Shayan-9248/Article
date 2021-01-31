# Generated by Django 3.1.5 on 2021-01-30 08:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20210130_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='s_category', to='core.category'),
        ),
    ]
