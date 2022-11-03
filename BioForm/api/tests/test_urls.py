from django.test import SimpleTestCase
from django.urls import resolve, reverse
from .. import views


class TestUrls(SimpleTestCase):

    def test_login_url_is_resolved(self):
        url = reverse('login-api')
        self.assertEquals(resolve(url).func.view_class, views.LoginView)

    def test_register_url_is_resolved(self):
        url = reverse('register-api')
        self.assertEquals(resolve(url).func.view_class, views.RegisterView)

    def test_bio_url_is_resolved(self):
        url = reverse('api-bio-view')
        self.assertEquals(resolve(url).func.view_class, views.BioView)

    def test_blog_url_is_resolved(self):
        url = reverse('api:apiblogview-list')
        self.assertEquals(resolve(url).func.__name__, views.BlogViewSet.__name__)