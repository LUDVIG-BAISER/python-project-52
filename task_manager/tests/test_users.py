from django.test import TestCase
from django.urls import reverse
from task_manager.users.models import Users


class CRUD_Users_Test(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = Users.objects.create_user(
            first_name='Vitya',
            last_name='loh',
            username='VL',
            email='VLoh@google.ru',
            password='666123'
        )
        cls.user2 = Users.objects.create_user(
            first_name='Mariya',
            last_name='Petrova',
            username='Masha003',
            email='masha@mail.ru',
            password='quni'
        )

    def test_SignUp(self):
        resp = self.client.get(reverse('create_user'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'users/registration.html')

        resp = self.client.post(reverse('create_user'), {
            'first_name': 'SIN',
            'last_name': 'DEAVOLA',
            'username': '228_loh',
            'password1': 'PROGREV_KOLTA',
            'password2': 'PROGREV_KOLTA',
        })
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('login'))
        self.assertEqual(Users.objects.count(), 3)

    def test_ListUsers(self):
        resp = self.client.get(reverse('home_users'))
        self.assertEqual(len(resp.context['users']), 2)

    def test_UpdateUser(self):
        user = Users.objects.get(username='VL')
        resp = self.client.get(reverse('update_user', kwargs={'pk': user.id}))
        self.assertEqual(resp.status_code, 302)

        self.client.force_login(user)
        resp = self.client.post(reverse('update_user', kwargs={'pk': user.id}), {
            'first_name': 'Petya',
            'last_name': 'Piter',
            'username': 'Petr1',
            'password1': 'lovePiter123',
            'password2': 'lovePiter123',
        })
        self.assertEqual(resp.status_code, 302)
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'Petya')

    def test_DeleteUser(self):
        user = Users.objects.get(username='Masha003')
        resp = self.client.get(reverse('delete_user', kwargs={'pk': user.id}))
        self.assertEqual(resp.status_code, 302)

        self.client.force_login(user)
        resp = self.client.post(reverse('delete_user', kwargs={'pk': user.id}))
        self.assertRedirects(resp, reverse('home_users'))
        self.assertEqual(Users.objects.count(), 1)
