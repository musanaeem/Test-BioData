from rest_framework.test import APITestCase
from django.urls import reverse

class TestSetup(APITestCase):

    def setUp(self):
        self.register_url = reverse('register-api')
        self.login_url = reverse('login-api')
        self.bio_url = reverse('api-bio-view')

        self.user_data = {
            'email':"musa.naeem@arbisoft.com",
            'password':"kaneki",
            'username':"musanaeem",
            'date_of_birth': "1996-11-12",
        }

        self.bio_data = {
            'name' : "Musa Naeem",
            'address' : "random Address",
            'description' : "description"
        }

        return super().setUp()

    def tearDown(self):


        return super().tearDown()