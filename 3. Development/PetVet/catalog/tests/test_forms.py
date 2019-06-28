from parameterized import parameterized
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from PetVet import forms

from django.test import Client
import unittest

login_existing_credentials = [("testuserW0", "secretW"),
                             ("testuserX0", "secretX"),
                             ("testuserY0", "secretY"),
                             ("testuserZ0", "secretZ")]

test_case_data_wrong_login = {
    "non_existing_login":   [("felipe", "felipe", False),
                             ("ANA12", "ANA12", False),
                             ("testuserA", "testuserA", False)
                            ],
    "wrong_password_login": [("testuser1", "qwerty", False),
                             ("testuser2", "not correct", False),
                             ("testuser3", "c2h$osn82/", False)
                            ],
    "wrong_username_existing_password_login": [("testuser!", "secretW", False),
                             ("test2", "secretX", False),
                             ("ingeSoft", "secretY", False)
                            ],
    "existing_login":       [("testuserW0", "secretW", True),
                             ("testuserX0", "secretX", True),
                             ("testuserY0", "secretY", True),
                             ("testuserZ0", "secretZ", True)]
}

#-------------------- TESTING LOGIN -----------------------#

def login_test_template(*args):
    def test(self):
        self.asser_login_info(*args)
    return test

class LoginTest(unittest.TestCase):
    # Creating predefined users to the check the login works
    @classmethod
    def setUpClass(cls):
        for login_data in login_existing_credentials:
            username, password = login_data
            
            cls.addCredential = {
                'username': username,
                'email': 'emails',
                'password': password
            }
            print(cls.addCredential)
            User.objects.create_user(username=username, password=password)

    # Creating a new client before EVERY TEST
    def setUp(self):
        self.client = Client()
    
    # Function will receive data and should return false should the user not exist and true should the user exist
    def asser_login_info(self, enteredUsername, enteredPassword, userExists):
        enteredCredentials = {
            'username': enteredUsername,
            'password': enteredPassword
        }
        response = self.client.post(reverse('login_page'), enteredCredentials, follow=True)
        self.assertEqual(response.context['user'].is_authenticated, userExists)


    # Will delete all the users created in setUpClass
    @classmethod
    def tearDownClass(cls):
        for login_data in login_existing_credentials:
            username, password = login_data
            u = User.objects.get(username = username)
            print(u)
            u.delete()


# Will iterate through the test cases and pass the arguments to the template
for behaviour, test_cases in test_case_data_wrong_login.items():
    for login_data in test_cases:
        username, password, exists = login_data
        test_name = "test_{0}_{1}_{2}".format(behaviour, username, password)
        login_test_case = login_test_template(*login_data)
        setattr(LoginTest, test_name, login_test_case);


#-------------------- TESTING REGISTRATION -----------------------#

addCredential = {
    'username': 'Felix Oj',
    'email': 'foj@gmail.com',
    'password': 'mybirthday'
}

class RegistrationTest(TestCase):
    @classmethod
    def setUpClass(cls):
        print(addCredential)
        User.objects.create_user(username=addCredential['username'],
                                 email=addCredential['email'],
                                 password=addCredential['password'])

    """
    A GET to the register view uses the appropriate
    template and populates the registration form into the context.
    """
    def test_registration_get(self):
     
        response = self.client.get(reverse('register_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'auth/view.html')
        self.failUnless(isinstance(response.context['form'],
                                   forms.RegisterForm))

    """
    A POST to the register view with valid register data properly
    creates a new user and issues a redirect.
    """
    def test_registration_post_success(self):
        data = {
            'username': 'Raian Pagano',
            'email1': 'rpagano@gmail.com',
            'password': 'fox38DOG90'
        }
        response = self.client.post(reverse('register_page'), data)  
                                
        # Upon success will redirect to the registration_complete page
        #self.assertRedirects(response,
        #                     'http://127.0.0.1:8000%s' % reverse('login_page'))
    
    """
    A POST to the register view with an existing username does not
    create a user, and displays appropriate error messages.
    """
    def test_registration_post_failure_username_taken(self):
        data = {
            'username': addCredential['username'],
            'email': 'felixoj@gmail.com',
            'password': 'mydifferentbirthday'
        }
        
        response = self.client.post(reverse('register_page'), data)                                    
        self.assertEqual(response.status_code, 200)
        self.failIf(response.context['form'].is_valid())        #Should not be valid!
        self.assertFormError(response, 'form', field=None,      #Appropiate error message
                             errors="Username already taken")
   
  
    # EL EMAIL VA A SER SOLAMENTE @GMAIL.COM???

    @classmethod
    def tearDownClass(cls):
        username = addCredential['username']
        u = User.objects.get(username = username)
        print(u)
        u.delete()