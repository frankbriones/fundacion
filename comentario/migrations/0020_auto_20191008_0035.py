# Generated by Django 2.1.1 on 2019-10-08 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comentario', '0019_auto_20191008_0028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='estado',
            field=models.SmallIntegerField(blank=True, choices=[(0, 'Activo'), (1, 'Inactivo')], default=0, null=True),
        ),
    ]
