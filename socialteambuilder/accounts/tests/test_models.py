from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.test import TestCase

from ..models import User, Skill


class UserModelTests(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(
            email='user1@email.com',
            first_name='User1',
            password='password123'
        )
        python_skill = Skill.objects.create(
            name="python"
        )
        javascript_skill = Skill.objects.create(
            name="javascript"
        )
    
    def test_user_created(self):
        users = User.objects.all()
        self.assertEqual(len(users), 1)
    
    def test_user_is_not_active(self):
        user = User.objects.get(id=1)
        self.assertEqual(user.is_active, False)

    def test_update_user(self):
        user = User.objects.get(id=1)
        user.last_name = 'User1LastName'
        user.avatar = SimpleUploadedFile(
            name='new_avatar_xyz.jpg', 
            content=open(__file__, 'rb').read(), 
            content_type='image/jpeg'
        )
        user.about = 'A little about user 1...'
        user.skills.add(1, 2)
        user.is_active = True
        user.save()
        self.assertEqual(user.last_name, 'User1LastName')
        self.assertEqual(user.avatar.name[:22], 'avatars/new_avatar_xyz')
        self.assertEqual(user.about, 'A little about user 1...')
        self.assertEqual(user.skills.count(), 2)
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_admin, False)


class SkillModelTests(TestCase):
    def setUp(self):
        python_skill = Skill.objects.create(
            name="python"
        )
        javascript_skill = Skill.objects.create(
            name="javascript"
        )
    
    def test_integrity_error(self):
        with self.assertRaises(IntegrityError):
            duplicate = Skill.objects.create(
                name='python'
            )
    