# Generated by Django 3.2.6 on 2021-09-08 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examfee', '0015_examfeepaid_transaction_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sublist',
            name='course',
            field=models.CharField(choices=[('1', 'BCA'), ('2', 'BCom'), ('3', 'Bsc'), ('4', 'BBA')], max_length=10),
        ),
    ]