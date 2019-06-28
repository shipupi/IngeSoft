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

#-------------------- TESTING LOGIN -----------------------#

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
                                'auth/view.html')
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
            print("TO BE IMPLEMENTED")
            #self.assertRedirects(response, reverse('home_page'))        

    # Will delete all the users created in setUpClass
    @classmethod
    def tearDownClass(cls):
        for login_data in existing_credentials:
            username, email, password = login_data
            u = User.objects.get(username = username)
            print(u)
            u.delete()


# Will iterate through the test cases and pass the arguments to the template
for behaviour, test_cases in test_case_data_login.items():
    for login_data in test_cases:
        username, password, exists = login_data
        test_name = "test_{0}_{1}_{2}".format(behaviour, username, password)
        login_test_case = login_test_template(*login_data)
        setattr(LoginTest, test_name, login_test_case);


#-------------------- TESTING REGISTRATION -----------------------#

username_error = "Username already taken"
password_error = "Passwords don't match"
gmail_error = "Email has to be gmail"
email_taken_error = "Email already taken"

test_case_data_invalid_registration = {
    "taken_username":           [("testuserW0", "mydifferentbirthday", "mydifferentbirthday", "felixoj@gmail.com", username_error),
                                 ("testuserW0", "pass1", "pass2", "testy@gmail.com", username_error),
                                 ("testuserZ0", "12nSdos2", "12nSdos2", "testZ@gmail.com", username_error)
                                ],
    "non_matching_passwords":   [("testuser0Y", "qwerty", "qwwerty", "valid@email.com", password_error),
                                 ("AllFire", "awesome", "notawesome", "cool@gmail.com", password_error),
                                 ("NEW", "random", "234random", "random@gmail.com", password_error)
                                ],
    "invalid_email":            [("user", "pass", "pass", "user@yahoo.com", gmail_error),
                                 ("testuser0Z", "234", "234", "user@google.com", gmail_error),
                                 ("testing", "p", "p", "invalidemail@something.com", gmail_error)
                                ],
    "email_taken":              [("test1", "1231!!", "1231!!", "X@gmail.com", email_taken_error),
                                 ("test2", "pass2", "pass2", "W@gmail.com", email_taken_error),
                                 ("testuser0X", "secret", "secret", "Z@gmail.com", email_taken_error)
                                ]
}

def registration_test_template(*args):
    def test(self):
        self.assert_incorrect_registration_info(*args)
    return test

class RegistrationTest(TestCase):
    @classmethod
    def setUpClass(cls):
        for register_data in existing_credentials:
            username, email, password = register_data
    
            User.objects.create_user(username=username, email=email, password=password)

    """
    A GET to the register view uses the appropriate
    template and populates the registration form into the context.
    """
    def test_registration_view_get(self):
     
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
            'username': 'Raian Paganos',
            'password': 'fox38DOG90',
            'password2': 'fox38DOG90',
            'email': 'rpaganos@gmail.com'
        }
        response = self.client.post(reverse('register_page'), data)  
                                
        # Upon success will redirect to the registration_complete page
        self.assertRedirects(response, reverse('register_complete_page'))
    
    """
    A POST to the register view with an existing username does not
    create a user, and displays appropriate error messages.
    """
    def assert_incorrect_registration_info(self, username, password1, password2, email, error):
        data = {
            'username': username,
            'password': password1,
            'password2': password2,
            'email': email
        }
        response = self.client.post(reverse('register_page'), data)                                    
        self.assertEqual(response.status_code, 200)
        self.failIf(response.context['form'].is_valid())        #Should not be valid!
        self.assertFormError(response, 'form', field=None,      #Appropiate error message
                             errors=error)
   
  
    # EL EMAIL VA A SER SOLAMENTE @GMAIL.COM???

    @classmethod
    def tearDownClass(cls):
        for registration_data in existing_credentials:
            username, email, password = registration_data
            u = User.objects.get(username = username)
            print(u)
            u.delete()


# Will iterate through the test cases of incorrect register data and pass the arguments to the template
for behaviour, test_cases in test_case_data_invalid_registration.items():
    for invalid_registration_data in test_cases:
        username, password1, password2, email, error = invalid_registration_data
        test_name = "test_{0}_{1}_{2}_{3}".format(behaviour, username, password1, email)
        registration_test_case = registration_test_template(*invalid_registration_data)
        setattr(RegistrationTest, test_name, registration_test_case);

