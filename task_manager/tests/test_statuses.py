from django.test import TestCase
from django.urls import reverse
from task_manager.statuses.models import Statuses
from task_manager.users.models import Users


class CRUD_Statuses_Test(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = Users.objects.create_user(
            username='admin',
            first_name='Vasya',
            last_name='Pupkin',
            email='vasya@test.com',
            password='secret123'
        )
        Statuses.objects.create(name='status1')
        Statuses.objects.create(name='status2')
        Statuses.objects.create(name='status3')

    def setUp(self):
        self.client.force_login(self.user)

    def test_access(self):
        self.client.logout()
        resp1 = self.client.get(reverse('create_status'))
        self.assertEqual(resp1.status_code, 302)
        resp2 = self.client.get(reverse('home_statuses'))
        self.assertEqual(resp2.status_code, 302)
        resp3 = self.client.get(reverse('update_status', kwargs={'pk': 1}))
        self.assertEqual(resp3.status_code, 302)
        resp4 = self.client.get(reverse('delete_status', kwargs={'pk': 1}))
        self.assertEqual(resp4.status_code, 302)

        self.client.force_login(self.user)
        resp1 = self.client.get(reverse('create_status'))
        self.assertEqual(resp1.status_code, 200)
        resp2 = self.client.get(reverse('home_statuses'))
        self.assertEqual(resp2.status_code, 200)
        resp3 = self.client.get(reverse('update_status', kwargs={'pk': 1}))
        self.assertEqual(resp3.status_code, 200)
        resp4 = self.client.get(reverse('delete_status', kwargs={'pk': 1}))
        self.assertEqual(resp4.status_code, 200)

    def test_CreateStatus(self):
        resp = self.client.post(reverse('create_status'), {'name': 'new_status'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Statuses.objects.count(), 4)

    def test_ListStatuses(self):
        resp = self.client.get(reverse('home_statuses'))
        self.assertEqual(len(resp.context['statuses']), 3)

    def test_UpdateStatus(self):
        status = Statuses.objects.get(pk=1)
        self.client.post(reverse('update_status', kwargs={'pk': 1}), {'name': 'updated'})
        status.refresh_from_db()
        self.assertEqual(status.name, 'updated')

    def test_DeleteStatus(self):
        self.assertEqual(Statuses.objects.count(), 3)
        self.client.post(reverse('delete_status', kwargs={'pk': 3}))
        self.assertEqual(Statuses.objects.count(), 2)
