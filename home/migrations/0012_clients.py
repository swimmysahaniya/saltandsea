# Generated by Django 5.0.6 on 2024-07-19 10:45

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_testimonial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='clients')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
