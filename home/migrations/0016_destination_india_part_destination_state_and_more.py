# Generated by Django 5.0.6 on 2024-07-24 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_faqs'),
    ]

    operations = [
        migrations.AddField(
            model_name='destination',
            name='india_part',
            field=models.CharField(default='abc', max_length=100),
        ),
        migrations.AddField(
            model_name='destination',
            name='state',
            field=models.CharField(default='abc', max_length=100),
        ),
        migrations.AddField(
            model_name='destination',
            name='tags',
            field=models.CharField(blank=True, default='abc', max_length=100, null=True),
        ),
    ]
