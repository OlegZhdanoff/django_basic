# Generated by Django 2.2.17 on 2020-12-22 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_auto_20201222_0608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='photo',
            field=models.ImageField(blank=True, upload_to='products/', verbose_name='Фото'),
        ),
    ]