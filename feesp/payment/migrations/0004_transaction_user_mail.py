# Generated by Django 3.2.6 on 2021-09-02 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_auto_20210902_1152'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='user_mail',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
