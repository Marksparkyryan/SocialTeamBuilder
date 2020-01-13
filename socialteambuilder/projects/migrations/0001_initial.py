# Generated by Django 3.0.2 on 2020-01-12 07:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(max_length=2000)),
                ('time_estimate', models.IntegerField()),
                ('applicant_requirements', models.TextField(max_length=2000)),
                ('status', models.CharField(choices=[('A', 'Open'), ('B', 'Closed'), ('C', 'Complete')], max_length=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='projects', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=2000)),
                ('status', models.CharField(choices=[('E', 'Empty'), ('F', 'Filled')], max_length=1)),
                ('time_estimate', models.IntegerField()),
                ('slug', models.SlugField(blank=True, editable=False)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project')),
                ('skills', models.ManyToManyField(related_name='positions', to='accounts.Skill')),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('A', 'Accepted'), ('R', 'Rejected'), ('U', 'Undecided')], max_length=1)),
                ('position', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='projects.Position')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'position')},
            },
        ),
    ]