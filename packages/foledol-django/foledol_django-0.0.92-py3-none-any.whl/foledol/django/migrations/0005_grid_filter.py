# Generated by Django 2.2 on 2022-05-12 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django', '0004_auto_20220212_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='grid',
            name='filter',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]
