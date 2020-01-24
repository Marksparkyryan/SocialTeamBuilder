import json
import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.test import TestCase
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from..forms import UserUpdateForm
from ..models import User
from ..views import account_activation_token

class RegisterTests(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(
            email='user1@email.com',
            first_name='User1',
            password='password123'
        )
        user1.is_active = True
        user1.save()

    def test_user_create_token_activate_cycle(self):
        resp = self.client.post(
            reverse('accounts:register'),
            data={
                'email': 'user2@email.com',
                'first_name': 'User2',
                'password1': 'password123',
                'password2': 'password123'
            },
            follow=True
        )
        self.assertEqual(resp.status_code, 200)  
        self.assertTemplateUsed(resp, 'accounts/check_inbox.html')  
        self.assertContains(resp, "You've registered!")
        user = User.objects.get(email='user2@email.com')
        self.assertFalse(user.is_active)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        resp = self.client.get(
            path=reverse('accounts:activate', kwargs={
                'uidb64': uid,
                'token': token
            }), 
            follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'accounts/edit_profile.html')


class LoginTests(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(
            email='user1@email.com',
            first_name='User1',
            password='password123'
        )
        user1.is_active = True
        user1.save()
    
    def test_login_and_redirect(self):
        resp = self.client.post(
            reverse('login'),
            data={
                'username': 'user1@email.com',
                'password': 'password123'
            },
            follow=True
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'projects/dashboard.html')
    

class UpdateUserTests(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(
            email='user1@email.com',
            first_name='User1',
            password='password123'
        )
        user1.is_active = True
        user1.save()
    
    def test_updating_user_info(self):
        self.client.login(
            username='user1@email.com',
            password='password123'
        )
        resp = self.client.post(
            reverse('accounts:updateuser'),
            data={
                'about': 'This is a new me',
                'first_name': 'Mark',
                'last_name': 'Ryan',
                'form-TOTAL_FORMS': 1, 
                'form-INITIAL_FORMS': 0 
            },
                follow=True
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'accounts/profile.html')
        self.assertContains(resp, 'This is a new me')
        self.assertContains(resp, "Profile updated successfully")
    
    def test_update_avatar(self):
        self.client.login(
            username='user1@email.com',
            password='password123'
        )
        old = User.objects.get(id=1).avatar
        file_path = os.path.dirname(__file__) + '/new_avatar_xyz.jpg'
        with open(file_path, 'rb') as avatar:
            resp = self.client.post(
                reverse('accounts:updateuser'),
                {'id_avatar':avatar},
                # content_type='multipart/form-data',
                HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                follow=False
                )
        new = User.objects.get(id=1).avatar
        self.assertNotEqual(old, new)


class ProfileTests(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(
            email='user1@email.com',
            first_name='User1',
            password='password123'
        )
        user1.is_active = True
        user1.save()
    
    def test_profile_view(self):
        self.client.login(
                username='user1@email.com',
                password='password123'
            )
        resp = self.client.get(
            reverse('accounts:profile', kwargs={'pk': 1})
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'accounts/profile.html')


        




