# Generated by Django 3.2.6 on 2021-09-02 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examfee', '0014_alter_examfeepaid_form_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='examfeepaid',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
