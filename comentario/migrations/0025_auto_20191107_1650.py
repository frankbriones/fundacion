# Generated by Django 2.2.6 on 2019-11-07 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comentario', '0024_auto_20191008_0306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='estado',
            field=models.SmallIntegerField(blank=True, choices=[(1, 'Inactivo'), (0, 'Activo')], default=0, null=True),
        ),
    ]
