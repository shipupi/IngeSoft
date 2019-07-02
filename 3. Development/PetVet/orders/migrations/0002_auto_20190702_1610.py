# Generated by Django 2.2.3 on 2019-07-02 16:10

import creditcards.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='cc_expiry',
            field=creditcards.models.CardExpiryField(default='01/01', verbose_name='expiration date'),
        ),
    ]