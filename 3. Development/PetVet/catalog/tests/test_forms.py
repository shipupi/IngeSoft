from django.contrib.auth.models import User
from django.urls import reverse

from django.test import TestCase
from django.test import Client

class LoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}

        #Creating a the user with username and password specified above
        User.objects.create_user(**self.credentials)
    
    def test_incorrect_login(self):
        incorrectCredentials = {
            'username': 'testuser',
            'password': 'incorrectPassword'
        }

        # send login data
        response = self.client.post(reverse('login_page'), incorrectCredentials, follow=True)
      
        # should NOT be logged in now
        self.assertFalse(response.context['user'].is_authenticated)

    # AHORA NO ANDA PORQUE SE ESTA HACIENDO UN REDIRECT A HOME QUE NO EXISTE
    # EL RESPONSE DA STATUS_CODE 404
    # CUANDO SACO EL REDIRECT ANDA ESTE TEST
    def test_correct_login(self):
        correctCredentials = self.credentials

        # send login data
        response = self.client.post(reverse('login_page'), correctCredentials, follow=True)
        
        # should be logged in now
        self.assertTrue(response.context['user'].is_authenticated)