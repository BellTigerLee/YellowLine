# Generated by Django 5.0.3 on 2024-04-07 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camapp', '0010_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to='media/'),
        ),
    ]
