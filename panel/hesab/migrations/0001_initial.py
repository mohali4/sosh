# Generated by Django 4.1.5 on 2023-02-01 14:39

from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models
import hesab.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='node',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('host', models.CharField(max_length=100)),
                ('port', models.IntegerField()),
                ('secret', models.TextField()),
                ('ssh_hostname', models.CharField(blank=True, default=None, max_length=30)),
            ],
            options={
                'verbose_name': 'سرور',
                'verbose_name_plural': 'سرورها',
            },
        ),
        migrations.CreateModel(
            name='period',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('days', models.IntegerField()),
                ('value', models.IntegerField()),
                ('users', models.IntegerField()),
                ('info', models.TextField(blank=True, default=None)),
            ],
            options={
                'verbose_name': 'محصول',
                'verbose_name_plural': 'محصولات',
            },
        ),
        migrations.CreateModel(
            name='vuser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('phonenumber', models.CharField(blank=True, max_length=13)),
                ('info', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'کاربر',
                'verbose_name_plural': 'کاربران',
            },
        ),
        migrations.CreateModel(
            name='transfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(default=hesab.models._password, max_length=15)),
                ('payed', models.BooleanField(default=False, verbose_name='پرداخت')),
                ('fake_payed', models.BooleanField(default=True, verbose_name='در هر صورت فعال شود')),
                ('start', django_jalali.db.models.jDateField(default=hesab.models._now, verbose_name='شروع')),
                ('info', models.TextField(blank=True, default=None, verbose_name='توضیحات')),
                ('config', models.TextField(blank=True, default='', verbose_name='کانفیگ')),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hesab.node', verbose_name='سرور')),
                ('period', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hesab.period', verbose_name='محصول')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hesab.vuser', verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'خرید',
                'verbose_name_plural': 'خریدها',
            },
        ),
    ]
