# Generated by Django 4.2.10 on 2025-05-08 23:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articles', '0002_tag_alter_article_options_article_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to='articles/covers/'),
        ),
        migrations.AddField(
            model_name='article',
            name='favorites',
            field=models.ManyToManyField(blank=True, related_name='favorite_articles', to=settings.AUTH_USER_MODEL),
        ),
    ]
