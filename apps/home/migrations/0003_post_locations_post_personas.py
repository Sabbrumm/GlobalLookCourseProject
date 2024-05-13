# Generated by Django 5.0.4 on 2024-05-12 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
        ('home', '0002_post_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='locations',
            field=models.ManyToManyField(to='api.geolocation'),
        ),
        migrations.AddField(
            model_name='post',
            name='personas',
            field=models.ManyToManyField(to='api.persona'),
        ),
    ]
