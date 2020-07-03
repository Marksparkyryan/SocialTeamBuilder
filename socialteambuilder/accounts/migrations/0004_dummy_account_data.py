import random

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError, transaction


from django.db import migrations

FIRST_NAMES = ['John', 'Steph', 'Steve', 'Michelle', 'Jack', 'Sara', 'Paul']
LAST_NAMES = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
ABOUT = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Sit amet cursus sit amet dictum. Vitae elementum curabitur vitae nunc. Dui ut ornare lectus sit. Faucibus purus in massa tempor. Viverra mauris in aliquam sem fringilla ut morbi. Nunc eget lorem dolor sed viverra. Eleifend donec pretium vulputate sapien nec. Dapibus ultrices in iaculis nunc sed augue lacus viverra. Viverra mauris in aliquam sem. Porttitor lacus luctus accumsan tortor. Ut porttitor leo a diam sollicitudin tempor id. A iaculis at erat pellentesque adipiscing commodo elit at. Tellus molestie nunc non blandit massa enim. Orci eu lobortis elementum nibh tellus. Quam vulputate dignissim suspendisse in est. Condimentum mattis pellentesque id nibh tortor id aliquet lectus. Quisque egestas diam in arcu cursus euismod quis. Nunc mattis enim ut tellus."

def forwards(apps, schema_editor):
    if settings.USE_DATA_MIGRATIONS:
        MyModel = apps.get_model('accounts', 'User')
        for _ in range(9):
            while True:
                try:
                    with transaction.atomic():
                        first = random.choice(FIRST_NAMES)
                        last = random.choice(LAST_NAMES)
                        email = first + last + '@fakemail.com'
                        password = make_password('ds80g7d679gsdd7g86gsd')
                        user = MyModel.objects.create(
                            email=email, 
                            first_name=first, 
                            password=password,
                            last_name=last,
                            about=ABOUT,
                            is_active=True
                        )
                        user.save()

                except IntegrityError:
                    print('Duplicate user generated, trying again...')
                    continue
                
                break
        
        try:
            with transaction.atomic():
                first = 'Guest'
                last = 'Account'
                email = first + last + '@fakemail.com'
                password = make_password('ds80g7d679gsdd7g86gsd')
                user = MyModel.objects.create(
                    email=email, 
                    first_name=first, 
                    password=password,
                    last_name=last,
                    about=ABOUT,
                    is_active=True
                )
                user.save()

        except Exception as e:
            print(e)
            pass


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20200627_0447'),
    ]

    operations = [
        migrations.RunPython(forwards),
    ]
