# Generated by Django 4.1.3 on 2022-11-28 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ifsolve', '0002_item_co_elaboradores_remove_item_elaborador_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='co_elaboradores',
            field=models.ManyToManyField(blank=True, related_name='co_elaboradores', to='ifsolve.elaborador'),
        ),
    ]