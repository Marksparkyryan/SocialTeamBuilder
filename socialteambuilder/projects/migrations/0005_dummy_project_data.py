import random

from django.conf import settings
from django.db import migrations, transaction
from django.utils.text import slugify

PROJECT_NAMES = ['Alpha Accounting', 'Beta Boarding', 'Charlie Communications', 'Delta Data', 'Echo Energy', 'Foxtrot Files', 'Golf Gal', 'Hotel Himalayas', 'India Internet', 'Juliett Journalism']
DESCRIPTION = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
POSITION_NAMES = ['Back-End Developer', 'Front-End Developer', 'Team Lead', 'UX', 'Tester', 'Operations', 'Graphic Design', 'Systems Admin', 'Mobile', 'UI', 'Data Architect', 'Cloud Architect', 'DevOps', 'QA' ]


def forwards_project(apps, schema_editor):
    if settings.USE_DATA_MIGRATIONS:
        project_model = apps.get_model('projects', 'Project')
        user_model = apps.get_model('accounts', 'User')

        for i in range(10):
            try:
                with transaction.atomic():
                    project = project_model.objects.create(
                        owner=user_model.objects.all()[i],
                        title=PROJECT_NAMES[i],
                        description=DESCRIPTION,
                        time_estimate=random.randint(1, 1000),
                        applicant_requirements=DESCRIPTION,
                        status='A',
                        slug=slugify(PROJECT_NAMES[i], allow_unicode=True)
                    )

            except Exception as e:
                print(e)
                pass

def forwards_position(apps, schema_editor):
    if settings.USE_DATA_MIGRATIONS:
        position_model = apps.get_model('projects', 'Position')
        project_model = apps.get_model('projects', 'Project')
        skill_model = apps.get_model('accounts', 'Skill')

        for project in project_model.objects.all():
            for _ in range(3):
                try:
                    with transaction.atomic():
                        pos_name = random.choice(POSITION_NAMES)
                        position = position_model.objects.create(
                            project=project,
                            title= pos_name,
                            description=DESCRIPTION,
                            status='E',
                            time_estimate=random.randint(1,1000),
                            slug=slugify(pos_name, allow_unicode=True)
                        )
                        position.skills.set(random.choices(skill_model.objects.all(), k=3))
                        position.save()

                except Exception as e:
                    print(e)
                    pass

def forwards_application(apps, schema_editor):
    if settings.USE_DATA_MIGRATIONS:
        application_model = apps.get_model('projects', 'Application')
        position_model = apps.get_model('projects', 'Position')
        user_model = apps.get_model('accounts', 'User')

        for user in user_model.objects.all():
            try:
                with transaction.atomic():
                    application_model.objects.create(
                        user=user,
                        position=random.choice(position_model.objects.all()),
                        status='U',
                    )

            except Exception as e:
                print(e)
                pass


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20200627_0435'),
    ]

    operations = [
        migrations.RunPython(forwards_project),
        migrations.RunPython(forwards_position),
        migrations.RunPython(forwards_application)
    ]
