# Generated by Django 2.1.1 on 2019-09-04 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comentario', '0002_comentario_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='contenido',
            field=models.CharField(max_length=50),
        ),
    ]
