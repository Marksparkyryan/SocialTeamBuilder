# Generated by Django 3.0.2 on 2020-06-27 04:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200627_0435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolioproject',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='portfolio_projects', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
