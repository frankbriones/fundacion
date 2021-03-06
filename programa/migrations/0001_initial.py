# Generated by Django 2.2.6 on 2019-11-07 21:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('donacion', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('persona', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=300, null=True)),
                ('estado', models.SmallIntegerField(choices=[(1, 'Inactivo'), (0, 'Activo')], null=True)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='programa/pictures')),
                ('created', models.DateField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('persona', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='persona.Persona')),
            ],
            options={
                'verbose_name': 'Programa',
                'verbose_name_plural': 'Programas',
            },
        ),
        migrations.CreateModel(
            name='Programa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=300, null=True)),
                ('fecha_programa', models.DateField(null=True, unique=True)),
                ('fecha_culminacion', models.DateField(null=True)),
                ('direccion', models.CharField(max_length=400, null=True)),
                ('estado', models.SmallIntegerField(choices=[(1, 'Inactivo'), (0, 'Activo')], default=True, null=True)),
                ('created', models.DateField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('evento', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='programa.Evento')),
                ('persona', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='persona.Persona')),
            ],
            options={
                'verbose_name': 'Evento',
                'verbose_name_plural': 'Eventos',
            },
        ),
        migrations.CreateModel(
            name='Detalle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cant', models.PositiveIntegerField(null=True)),
                ('created', models.DateField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('producto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='donacion.Producto')),
                ('programa', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='programa.Programa')),
                ('tipo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='donacion.Tipo')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedido', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Detalle de Evento',
                'verbose_name_plural': 'Detalles del Evento',
            },
        ),
    ]
