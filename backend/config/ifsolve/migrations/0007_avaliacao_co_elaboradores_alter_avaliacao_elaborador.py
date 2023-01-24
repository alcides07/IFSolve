# Generated by Django 4.1.3 on 2023-01-04 01:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ifsolve', '0006_alter_area_codigo_alter_area_nome_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='avaliacao',
            name='co_elaboradores',
            field=models.ManyToManyField(blank=True, to='ifsolve.elaborador'),
        ),
        migrations.AlterField(
            model_name='avaliacao',
            name='elaborador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='elaborador', to='ifsolve.elaborador'),
        ),
    ]