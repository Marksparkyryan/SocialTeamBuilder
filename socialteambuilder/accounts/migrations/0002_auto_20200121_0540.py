# Generated by Django 3.0.2 on 2020-01-21 05:40

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='about',
            field=markdownx.models.MarkdownxField(default='A little about you...', max_length=2000),
        ),
    ]
