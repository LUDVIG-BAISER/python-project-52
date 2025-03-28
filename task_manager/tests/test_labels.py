from django.test import TestCase
from task_manager.labels.models import Labels
from task_manager.users.models import Users
from django.urls import reverse


class CRUD_Labels_Test(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = Users.objects.create_user(
            username='Semen_pes',
            first_name='Semen',
            last_name='Efr',
            email='root@gav.ru',
            password='ilovekitty'
        )
        Labels.objects.create(name='label1')
        Labels.objects.create(name='label2')
        Labels.objects.create(name='label3')

    def setUp(self):
        self.client.force_login(self.user)

    def test_access(self):
        '''Незалогиненные пользователи получают редирект'''
        self.client.logout()
        resp1 = self.client.get(reverse('create_label'))
        self.assertEqual(resp1.status_code, 302)
        resp2 = self.client.get(reverse('home_labels'))
        self.assertEqual(resp2.status_code, 302)
        resp3 = self.client.get(reverse('update_label', kwargs={'pk': 1}))
        self.assertEqual(resp3.status_code, 302)
        resp4 = self.client.get(reverse('delete_label', kwargs={'pk': 1}))
        self.assertEqual(resp4.status_code, 302)

        '''Залогинимся'''
        self.client.force_login(self.user)
        resp1 = self.client.get(reverse('create_label'))
        self.assertEqual(resp1.status_code, 200)
        resp2 = self.client.get(reverse('home_labels'))
        self.assertEqual(resp2.status_code, 200)
        resp3 = self.client.get(reverse('update_label', kwargs={'pk': 1}))
        self.assertEqual(resp3.status_code, 200)
        resp4 = self.client.get(reverse('delete_label', kwargs={'pk': 1}))
        self.assertEqual(resp4.status_code, 200)

    def test_CreateLabel(self):
        resp = self.client.post(reverse('create_label'), {'name': 'gavgav'})
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('home_labels'))
        resp = self.client.get(reverse('home_labels'))
        self.assertEqual(len(resp.context['labels']), 4)

    def test_Listlabel(self):
        resp = self.client.get(reverse('home_labels'))
        self.assertEqual(len(resp.context['labels']), 3)

    def test_UpdateLabels(self):
        s1 = Labels.objects.get(pk=1)
        resp = self.client.post(
            reverse('update_label', kwargs={'pk': 1}),
            {'name': 'Updated label'}
        )
        self.assertEqual(resp.status_code, 302)
        s1.refresh_from_db()
        self.assertEqual(s1.name, 'Updated label')

    def test_DeleteStatus(self):
        self.assertEqual(Labels.objects.count(), 3)
        resp = self.client.post(reverse('delete_label', kwargs={'pk': 3}))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Labels.objects.count(), 2)
        self.assertEqual(Labels.objects.get(pk=1).name, 'label1')
        self.assertEqual(Labels.objects.get(pk=2).name, 'label2')
