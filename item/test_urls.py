from django.test import TestCase
from django.urls import reverse, resolve

from item import views


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
        self.assertEqual(resolve(path).func, views.about)

    def test_contact_url(self):
        path = reverse('contact')
        self.assertEqual(resolve(path).func, views.contact)

    def test_registration_url(self):
        path = reverse('registration')
        self.assertEqual(resolve(path).func, views.registration)

    def test_validateUser_url(self):
        path = reverse('validateUser')
        self.assertEqual(resolve(path).func, views.validateRegistrationDetails)

    def test_login_url(self):
        path = reverse('log')
        self.assertEqual(resolve(path).func, views.loginView)

    def test_authenticate_url(self):
        path = reverse('authenticate')
        self.assertEqual(resolve(path).func, views.authenticateUser)

    def test_logout_url(self):
        path = reverse('logout')
        self.assertEqual(resolve(path).func, views.logoutView)

    def test_account_url(self):
        path = reverse('account')
        self.assertEqual(resolve(path).func, views.account)

    def test_cleanHistory_url(self):
        path = reverse('cleanHistory')
        self.assertEqual(resolve(path).func, views.cleanHistory)
