from parameterized import parameterized
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from PetVet import forms

from django.test import Client

existing_credentials =      [("testuserW0", "W@gmail.com", "secretW"),
                             ("testuserX0", "X@gmail.com", "secretX"),
                             ("testuserY0", "Y@gmail.com", "secretY"),
                             ("testuserZ0", "Z@gmail.com", "secretZ")]

test_case_data_login = {
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

def login_test_template(*args):
    def test(self):
        self.assert_login_info(*args)
    return test

class LoginTest(TestCase):
    # Creating predefined users to the check the login works
    @classmethod
    def setUpClass(cls):
        for login_data in existing_credentials:
            username, email, password = login_data
            
            User.objects.create_user(username=username, email=email, password=password)

    # Creating a new client before EVERY TEST
    def setUp(self):
        self.client = Client()

    """
    A GET to the login view uses the appropriate
    template and populates the registration form into the context.
    """
    def test_login_view_get(self):
        response = self.client.get(reverse('login_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'auth/login.html')
        self.failUnless(isinstance(response.context['form'],
                                   forms.LoginForm))

    
    # Function will receive data and should return false should the user not exist and true should the user exist
    def assert_login_info(self, enteredUsername, enteredPassword, userExists):
        enteredCredentials = {
            'username': enteredUsername,
            'password': enteredPassword
        }
        response = self.client.post(reverse('login_page'), enteredCredentials, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].is_authenticated, userExists)

        # If the user exists, should redirect me to the home page
        if(userExists == True):
            self.assertRedirects(response, '/')        

    # Will delete all the users created in setUpClass
    @classmethod
    def tearDownClass(cls):
        for login_data in existing_credentials:
            username, email, password = login_data
            u = User.objects.get(username = username)
            u.delete()


# Will iterate through the test cases and pass the arguments to the template
for behaviour, test_cases in test_case_data_login.items():
    for login_data in test_cases:
        username, password, exists = login_data
        test_name = "test_{0}_{1}_{2}".format(behaviour, username, password)
        login_test_case = login_test_template(*login_data)
        setattr(LoginTest, test_name, login_test_case);
