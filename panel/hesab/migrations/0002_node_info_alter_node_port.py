# Generated by Django 4.1.5 on 2023-02-01 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hesab', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='info',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='node',
            name='port',
            field=models.IntegerField(default=2222),
        ),
    ]