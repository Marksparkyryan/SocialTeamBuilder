import random

from django.conf import settings
from django.db import migrations, transaction


def forwards(apps, schema_editor):
    if settings.USE_DATA_MIGRATIONS:
        portfolio = apps.get_model('accounts', 'PortfolioProject')
        users = apps.get_model('accounts', 'User')
        
        for user in users.objects.all():
            for i in range(1,4):
                try:
                    with transaction.atomic():
                        version = str(random.randint(0,1000))
                        portfolio.objects.create(
                            user=user,
                            name=user.first_name + ' Portfolio Project ' + version,
                            url='https://{}{}project{}.com'.format(user.first_name, user.last_name, version).lower()
                        )

                except Exception as e:
                    print(e)
                    pass


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_dummy_skills_data'),
    ]

    operations = [
        migrations.RunPython(forwards)
    ]
