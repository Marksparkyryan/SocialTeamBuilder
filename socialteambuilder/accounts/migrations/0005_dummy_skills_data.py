import random

from django.conf import settings
from django.db import migrations, transaction

SKILLS = ['sql', 'python', 'css', 'javascript', 'java', 'html', 'testing', 'design', 'oop', 'django', 'flask', 'security', 'api', 'rest', 'sass', 'git', 'bash', 'docker']

def forwards_skill(apps, schema_editor):
    if settings.USE_DATA_MIGRATIONS:
        skill_model = apps.get_model('accounts', 'Skill')
        for skill in SKILLS:
            try:
                with transaction.atomic():
                    skill_model.objects.create(
                        name=skill
                    )
            except Exception as e:
                print(e)
                pass

def forwards_user_skills(apps, schema_editor):
    if settings.USE_DATA_MIGRATIONS:
        user_model = apps.get_model('accounts', 'User')
        skill_model = apps.get_model('accounts', 'Skill')
        for user in user_model.objects.all():
            try:
                with transaction.atomic():
                    skills_list = [skill.id for skill in random.choices(skill_model.objects.all(), k=5)]
                    user.skills.set(skills_list)
                    user.save()
            except Exception as e:
                print(e)
                pass



class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_dummy_account_data'),
    ]

    operations = [
        migrations.RunPython(forwards_skill),
        migrations.RunPython(forwards_user_skills)
    ]
