# Generated by Django 5.0 on 2023-12-10 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_article_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='imageLink',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
