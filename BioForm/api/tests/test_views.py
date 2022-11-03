from .test_setup import TestSetup

class TestViews(TestSetup):

    def test_user_can_be_registered(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        
        self.assertEqual(response.data['email'], self.user_data['email'])
        self.assertEqual(response.data['username'], self.user_data['username'])
        self.assertEqual(response.data['date_of_birth'], self.user_data['date_of_birth'])
        self.assertEqual(response.status_code, 200)

    def test_user_cannot_login_without_data(self):
        response = self.client.post(self.login_url)

        self.assertEqual(response.status_code, 400)

    def test_user_can_login(self):
        self.client.post(self.register_url, self.user_data, format='json')
        response = self.client.post(self.login_url, self.user_data, format='json')

        self.assertEqual(response.status_code, 200)

    def authentication_user_and_add_bio(self):
        self.test_user_can_login()
        self.client.post(self.bio_url, self.bio_data, format='json')

    def test_bio_unauthenticated(self):
        response = self.client.get(self.bio_url)

        self.assertEqual(response.status_code, 403)

    def test_bio_GET(self):
        self.authentication_user_and_add_bio()

        response = self.client.get(self.bio_url)

        self.assertIn(response.status_code, [200, 404])
        self.assertEqual(response.data['name'], self.bio_data['name'])
        self.assertEqual(response.data['address'], self.bio_data['address'])
        self.assertEqual(response.data['description'], self.bio_data['description'])

    def test_bio_PATCH(self):
        self.authentication_user_and_add_bio()

        response = self.client.patch(self.bio_url, {'name': "Musa Naeem Sahaf"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], "Musa Naeem Sahaf")


    def test_bio_DELETE(self):
        self.authentication_user_and_add_bio()

        response = self.client.delete(self.bio_url)
        self.assertEqual(response.data['message'], "Deletion Successful!")