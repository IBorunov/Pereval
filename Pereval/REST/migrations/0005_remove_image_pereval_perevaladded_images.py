# Generated by Django 5.0.4 on 2024-04-24 19:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('REST', '0004_rename_coord_perevaladded_coords'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='pereval',
        ),
        migrations.AddField(
            model_name='perevaladded',
            name='images',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='REST.image'),
        ),
    ]