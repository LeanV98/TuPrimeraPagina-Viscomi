# Generated by Django 4.2.7 on 2023-12-20 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pagina', '0003_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avatar',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/'),
        ),
    ]