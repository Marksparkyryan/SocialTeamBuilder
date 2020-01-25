from django.test import TestCase
from django.urls import reverse

from ..models import Project, Position, Application
from accounts.models import User, Skill


class DashboardViewTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email='sparky@email.com',
            first_name='Mark',
            password='password123'
        )
        self.user1.is_active = True
        self.user1.skills.add(1)
        self.user1.save()
        self.user2 = User.objects.create_user(
            email='jess@email.com',
            first_name='Jess',
            password='password123'
        )
        self.user2.is_active = True
        self.user2.save()
        self.python = Skill.objects.create(
            name='python'
        )
        self.sql = Skill.objects.create(
            name='sql'
        )
        self.css = Skill.objects.create(
            name='css'
        )
        self.project_alpha = Project.objects.create(
            owner=self.user1,
            title='Alpha Project',
            description='This is project alpha',
            time_estimate=500,
            applicant_requirements='Project alpha requirements',
            status='A',
        )
        self.project_beta = Project.objects.create(
            owner=self.user2,
            title='Beta Project',
            description='This is project beta',
            time_estimate=500,
            applicant_requirements='Project beta requirements',
            status='A',
        )
        self.project_charlie = Project.objects.create(
            owner=self.user1,
            title='Charlie Project',
            description='This is project charlie',
            time_estimate=500,
            applicant_requirements='Project charlie requirements',
            status='A',
        )
        self.developer = Position.objects.create(
            project=self.project_alpha,
            title='Developer',
            description='Do dev stuff',
            time_estimate=500,
            status='E'
        )
        self.team_lead = Position.objects.create(
            project=self.project_beta,
            title='Team Lead',
            description='Do leading stuff',
            time_estimate=500,
            status='E'
        )
        self.developer.skills.add(1, 2)

    def test_length_products(self):
        self.client.login(
            username='sparky@email.com',
            password='password123'
        )
        resp = self.client.get(
            reverse('projects:dashboard', kwargs={
                'category':'all',
                'q':'all'
                }),
        )
        filtered = resp.context['filtered']
        self.assertEqual(len(filtered), 2)

    def test_position_filter(self):
        self.client.login(
            username='sparky@email.com',
            password='password123'
        )
        resp = self.client.get(
            reverse('projects:dashboard', kwargs={
                'category':'need',
                'q':'team-lead'
                }),
        )
        all_projects = resp.context['object_list']
        filtered = resp.context['filtered']
        self.assertEqual(len(all_projects), 2)
        self.assertEqual(len(filtered), 1)

    def test_personalized_filter(self):
        self.client.login(
            username='sparky@email.com',
            password='password123'
        )
        resp = self.client.get(
            reverse('projects:dashboard', kwargs={
                'category':'skills',
                'q':'skills'
                }),
        )
        all_projects = resp.context['object_list']
        filtered = resp.context['filtered']
        self.assertEqual(len(all_projects), 2)
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered.first(), Project.objects.get(id=1))


class SearchBarTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email='sparky@email.com',
            first_name='Mark',
            password='password123'
        )
        self.user1.is_active = True
        self.user1.skills.add(1)
        self.user1.save()
        self.user2 = User.objects.create_user(
            email='jess@email.com',
            first_name='Jess',
            password='password123'
        )
        self.user2.is_active = True
        self.user2.save()
        self.python = Skill.objects.create(
            name='python'
        )
        self.sql = Skill.objects.create(
            name='sql'
        )
        self.css = Skill.objects.create(
            name='css'
        )
        self.project_alpha = Project.objects.create(
            owner=self.user1,
            title='Alpha Project',
            description='This is project alpha',
            time_estimate=500,
            applicant_requirements='Project alpha requirements',
            status='A',
        )
        self.project_beta = Project.objects.create(
            owner=self.user2,
            title='Beta Project',
            description='This is project beta',
            time_estimate=500,
            applicant_requirements='Project beta requirements',
            status='A',
        )
        self.project_charlie = Project.objects.create(
            owner=self.user1,
            title='Charlie Project',
            description='This is project charlie',
            time_estimate=500,
            applicant_requirements='Project charlie requirements',
            status='A',
        )
        self.developer = Position.objects.create(
            project=self.project_alpha,
            title='Developer',
            description='Do dev stuff',
            time_estimate=500,
            status='E'
        )
        self.team_lead = Position.objects.create(
            project=self.project_beta,
            title='Team Lead',
            description='Do leading stuff',
            time_estimate=500,
            status='E'
        )
        self.developer.skills.add(1, 2)
    
    def test_search(self):
        self.client.login(
            username='sparky@email.com',
            password='password123'
        )
        resp = self.client.get(
            reverse('projects:searchbar'),
            data={'q':'python'},
            follow=True
        )
        filtered = resp.context['filtered']
        self.assertEqual(len(filtered), 1)
        resp = self.client.get(
            reverse('projects:searchbar'),
            data={'q':'badsearch'},
            follow=True
        )
        filtered = resp.context['filtered']
        self.assertEqual(len(filtered), 0)
    

class ApplicationListTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email='sparky@email.com',
            first_name='Mark',
            password='password123'
        )
        self.user1.is_active = True
        self.user1.skills.add(1)
        self.user1.save()
        self.user2 = User.objects.create_user(
            email='jess@email.com',
            first_name='Jess',
            password='password123'
        )
        self.user2.is_active = True
        self.user2.save()
        self.python = Skill.objects.create(
            name='python'
        )
        self.sql = Skill.objects.create(
            name='sql'
        )
        self.css = Skill.objects.create(
            name='css'
        )
        self.project_alpha = Project.objects.create(
            owner=self.user1,
            title='Alpha Project',
            description='This is project alpha',
            time_estimate=500,
            applicant_requirements='Project alpha requirements',
            status='A',
        )
        self.project_beta = Project.objects.create(
            owner=self.user2,
            title='Beta Project',
            description='This is project beta',
            time_estimate=500,
            applicant_requirements='Project beta requirements',
            status='A',
        )
        self.project_charlie = Project.objects.create(
            owner=self.user1,
            title='Charlie Project',
            description='This is project charlie',
            time_estimate=500,
            applicant_requirements='Project charlie requirements',
            status='A',
        )
        self.developer = Position.objects.create(
            project=self.project_alpha,
            title='Developer',
            description='Do dev stuff',
            time_estimate=500,
            status='E'
        )
        self.team_lead = Position.objects.create(
            project=self.project_beta,
            title='Team Lead',
            description='Do leading stuff',
            time_estimate=500,
            status='E'
        )
        self.developer.skills.add(1, 2)
        self.application1 = Application.objects.create(
            user=self.user2,
            position=self.developer,
            status='U',
        )
        self.application2 = Application.objects.create(
            user=self.user1,
            position=self.team_lead,
            status='U',
        )
    
    def test_all_applications(self):
        self.client.login(
            username='sparky@email.com',
            password='password123'
        )
        resp = self.client.get(
            reverse('projects:applications', kwargs={
                'box': 'inbox',
                'category': 'status',
                'q': 'u'
            })
        )
        applications = resp.context['filtered']
        self.assertEqual(len(applications), 1)

    def test_accepted_applications(self):
        self.client.login(
            username='sparky@email.com',
            password='password123'
        )
        resp = self.client.get(
            reverse('projects:applications', kwargs={
                'box': 'inbox',
                'category': 'status',
                'q': 'a'
            })
        )
        applications = resp.context['filtered']
        self.assertEqual(len(applications), 0)
        self.application1.status = 'A'
        self.application1.save()
        resp = self.client.get(
            reverse('projects:applications', kwargs={
                'box': 'inbox',
                'category': 'status',
                'q': 'a'
            })
        )
        applications = resp.context['filtered']
        self.assertEqual(len(applications), 1)


    

