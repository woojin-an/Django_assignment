# Generated by Django 5.1 on 2024-08-30 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0003_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='completed_image',
            field=models.ImageField(blank=True, null=True, upload_to='todo/', verbose_name='이미지'),
        ),
        migrations.AddField(
            model_name='todo',
            name='thumbnail',
            field=models.ImageField(blank=True, default='todo/no_image/NO-IMAGE.jpg', null=True, upload_to='todo/thumbnail', verbose_name='썸네일'),
        ),
    ]
