# Generated by Django 2.1.1 on 2019-09-25 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comentario', '0016_auto_20190925_1419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='estado',
            field=models.SmallIntegerField(blank=True, choices=[(0, 'Activo'), (1, 'Inactivo')], default=0, null=True),
        ),
    ]
