# Generated by Django 5.0.3 on 2024-04-07 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camapp', '0007_alter_post_options_remove_post_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(default='media/chauchaudog.jpg', upload_to=''),
        ),
    ]
