# Generated by Django 4.0.2 on 2022-03-10 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_news_views_alter_news_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='views',
            field=models.IntegerField(default=0, verbose_name='Просмотры'),
        ),
    ]