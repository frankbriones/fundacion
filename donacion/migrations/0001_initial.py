# Generated by Django 2.2.6 on 2019-11-07 21:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoria', models.CharField(max_length=50, null=True)),
                ('created', models.DateField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
            },
        ),
        migrations.CreateModel(
            name='Donacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('nombres', models.CharField(max_length=100, null=True)),
                ('apellido_paterno', models.CharField(max_length=100, null=True)),
                ('estado', models.SmallIntegerField(choices=[(1, 'Activo'), (0, 'Inactivo')], default=True, null=True)),
            ],
            options={
                'verbose_name': 'Donacion',
                'verbose_name_plural': 'Donaciones',
            },
        ),
        migrations.CreateModel(
            name='Tipo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'Tipo',
                'verbose_name_plural': 'Tipos',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=100, null=True)),
                ('fecha_expiracion', models.DateField(blank=True, default='12/12/2020', null=True)),
                ('cantidad', models.PositiveIntegerField(null=True)),
                ('estado', models.SmallIntegerField(blank=True, choices=[(1, 'Inactivo'), (0, 'Activo')], default=0, null=True)),
                ('stock', models.IntegerField(blank=True, default=0, null=True)),
                ('condicion', models.SmallIntegerField(blank=True, choices=[(0, 'Valida'), (1, 'Descompuesto')], default=0, null=True)),
                ('created', models.DateField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('categoria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='donacion.Categoria')),
                ('donacion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='donacion.Donacion')),
                ('tipo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='donacion.Tipo')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
            },
        ),
    ]