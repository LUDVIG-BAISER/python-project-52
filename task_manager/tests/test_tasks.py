from django.test import TestCase
from django.urls import reverse
from task_manager.users.models import Users
from task_manager.statuses.models import Statuses
from task_manager.labels.models import Labels


class CRUD_Tasks_Test(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = Users.objects.create_user(
            first_name='SIN',
            last_name='DEAVOLA',
            username='228_loh',
            email='root@preispodia.com',
            password='PROGREV_KOTLA'
        )
        cls.status = Statuses.objects.create(name='status1')
        cls.label = Labels.objects.create(name='label1')

    def setUp(self):
        self.client.force_login(self.user)

    def test_access(self):
        urls = [
            reverse('home_tasks'),
            reverse('create_task'),
            reverse('view_task', kwargs={'pk': 1}),
            reverse('update_task', kwargs={'pk': 1}),
            reverse('delete_task', kwargs={'pk': 1}),
        ]

        self.client.logout()  # Проверим сначала без логина
        for u in urls:
            resp = self.client.get(u)
            self.assertEqual(resp.status_code, 302)

        self.client.force_login(self.user)  # И потом с логином
        for u in urls:
            resp = self.client.get(u)

            self.assertIn(resp.status_code, [200, 404])
