from django.test import TestCase
from django.urls import reverse, resolve

from item import views
from item import forms


class TestUrls(TestCase):

    def test_index_url(self):
        path = reverse('index')
        self.assertEqual(resolve(path).func, views.index)

    def test_payment_url(self):
        path = reverse('payment', args=[1])  # Testing with itemId=1 as an example
        self.assertEqual(resolve(path).func, views.payment)

    def test_pay_url(self):
        path = reverse('pay', args=[1])  # Testing with itemId=1 as an example
        self.assertEqual(resolve(path).func, views.pay)

    def test_about_url(self):
        path = reverse('about')
        self.assertEqual(resolve(path).func, views.render_about_page)

    def test_contact_url(self):
        path = reverse('contact')
        self.assertEqual(resolve(path).func, views.render_contact_page)

    def test_registration_url(self):
        path = reverse('registration')
        self.assertEqual(resolve(path).func, views.render_registration_page)

    def test_validateUser_url(self):
        path = reverse('validateUser')
        self.assertEqual(resolve(path).func, forms.validate_registration_details)

    def test_login_url(self):
        path = reverse('log')
        self.assertEqual(resolve(path).func, views.loginiew)

    def test_authenticate_url(self):
        path = reverse('authenticate')
        self.assertEqual(resolve(path).func, forms.authenticate_user)

    def test_logout_url(self):
        path = reverse('logout')
        self.assertEqual(resolve(path).func, views.logout_view)

    def test_account_url(self):
        path = reverse('account')
        self.assertEqual(resolve(path).func, views.account)

    def test_cleanHistory_url(self):
        path = reverse('cleanHistory')
        self.assertEqual(resolve(path).func, views.clean_history)
