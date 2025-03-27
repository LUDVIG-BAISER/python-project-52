from django.test import TestCase
from task_manager.labels.models import Labels
from task_manager.users.models import Users
from django.urls import reverse


# Create your tests here.
class CRUD_Labels_Test(TestCase):
    def setUp(self):
        Users.objects.create(
            first_name='Semen',
            last_name='Efr',
            username='Semen_pes',
            email='root@gav.ru',
            password='ilovekitty'
        )
        self.user = Users.objects.get(id=1)
        Labels.objects.create(name='label1')
        Labels.objects.create(name='label2')
        Labels.objects.create(name='label3')

    # Проверка доступа незалогененым пользователям
    def test_access(self):
        '''Незалогинение пользователи получают редирект'''
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

    # CREATE - Создание новой метки
    def test_CreateLabel(self):
        self.client.force_login(self.user)
        '''Добавим статус'''
        resp = self.client.post(reverse('create_label'), {'name': 'gavgav'})
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('home_labels'))
        '''Проверяем добавлен ли новый статус'''
        resp = self.client.get(reverse('home_labels'))
        self.assertTrue(len(resp.context['labels']) == 4)

    # READ - список всех статусов
    def test_Listlabel(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse('home_labels'))
        self.assertTrue(len(resp.context['labels']) == 3)

    # UPDATE - обновление статуса
    def test_UpdateLabels(self):
        self.client.force_login(self.user)
        s1 = Labels.objects.get(pk=1)
        resp = self.client.post(reverse('update_label', kwargs={'pk': 1}),
                                {'name': 'Updated label'})
        self.assertEqual(resp.status_code, 302)
        s1.refresh_from_db()
        self.assertEqual(s1.name, 'Updated label')

    # DELETE - удаление статуса
    def test_DeleteStatus(self):
        self.client.force_login(self.user)
        self.assertEqual(Labels.objects.count(), 3)
        resp = self.client.post(
            reverse('delete_label', kwargs={'pk': 3})
        )
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Labels.objects.count(), 2)
        self.assertEqual(Labels.objects.get(pk=1).name, 'label1')
        self.assertEqual(Labels.objects.get(pk=2).name, 'label2')
