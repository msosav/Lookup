# Generated by Django 4.1 on 2022-10-15 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Aplicacion', '0002_rename_price_producto_precio'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='primer_comentario',
            field=models.CharField(default='N/A', max_length=200),
        ),
        migrations.AddField(
            model_name='producto',
            name='segundo_comentario',
            field=models.CharField(default='N/A', max_length=200),
        ),
    ]