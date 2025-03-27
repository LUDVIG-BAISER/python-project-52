from django.test import TestCase
from django.urls import reverse
from task_manager.statuses.models import Statuses
from task_manager.users.models import Users


# Create your tests here.
class CRUD_Statuses_Test(TestCase):
    def setUp(self):
        Users.objects.create(
            first_name='Alexey',
            last_name='Navalny',
            username='FBK',
            email='root@fbk.ru',
            password='iloveputin'
        )
        self.user = Users.objects.get(id=1)
        Statuses.objects.create(name='status1-work')
        Statuses.objects.create(name='status2-relax')
        Statuses.objects.create(name='status3-test')

    # Проверка доступа незалогененым пользователям
    def test_access(self):
        '''Незалогинение пользователи получают редирект'''
        resp1 = self.client.get(reverse('create_status'))
        self.assertEqual(resp1.status_code, 302)
        resp2 = self.client.get(reverse('home_statuses'))
        self.assertEqual(resp2.status_code, 302)
        resp3 = self.client.get(reverse('update_status', kwargs={'pk': 1}))
        self.assertEqual(resp3.status_code, 302)
        resp4 = self.client.get(reverse('delete_status', kwargs={'pk': 1}))
        self.assertEqual(resp4.status_code, 302)
        '''Залогинимся'''
        self.client.force_login(self.user)
        resp1 = self.client.get(reverse('create_status'))
        self.assertEqual(resp1.status_code, 200)
        resp2 = self.client.get(reverse('home_statuses'))
        self.assertEqual(resp2.status_code, 200)
        resp3 = self.client.get(reverse('update_status', kwargs={'pk': 1}))
        self.assertEqual(resp3.status_code, 200)
        resp4 = self.client.get(reverse('delete_status', kwargs={'pk': 1}))
        self.assertEqual(resp4.status_code, 200)

    # CREATE - Создание нового статуса
    def test_CreateStatus(self):
        self.client.force_login(self.user)
        '''Добавим статус'''
        resp = self.client.post(reverse('create_status'), {'name': 'status4'})
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('home_statuses'))
        '''Проверяем добавлен ли новый статус'''
        resp = self.client.get(reverse('home_statuses'))
        self.assertTrue(len(resp.context['statuses']) == 4)

    # READ - список всех статусов
    def test_ListStatuses(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse('home_statuses'))
        self.assertTrue(len(resp.context['statuses']) == 3)

    # UPDATE - обновление статуса
    def test_UpdateStatus(self):
        self.client.force_login(self.user)
        s1 = Statuses.objects.get(pk=1)
        resp = self.client.post(reverse('update_status', kwargs={'pk': 1}),
                                {'name': 'Updated Status'})
        self.assertEqual(resp.status_code, 302)
        s1.refresh_from_db()
        self.assertEqual(s1.name, 'Updated Status')

    # DELETE - удаление статуса
    def test_DeleteStatus(self):
        self.client.force_login(self.user)
        self.assertEqual(Statuses.objects.count(), 3)
        resp = self.client.post(
            reverse('delete_status', kwargs={'pk': 3})
        )
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Statuses.objects.count(), 2)
        self.assertEqual(Statuses.objects.get(pk=1).name, 'status1-work')
        self.assertEqual(Statuses.objects.get(pk=2).name, 'status2-relax')
