# Generated by Django 4.1 on 2022-11-29 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0006_moods_addr_moods_ip_alter_moods_create_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moods',
            name='create_date',
            field=models.DateTimeField(auto_now=True, verbose_name='發佈時間'),
        ),
    ]
