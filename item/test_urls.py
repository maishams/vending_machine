from django.test import TestCase
from django.urls import reverse, resolve, NoReverseMatch
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from item import views
from item import forms
from item.models import Item


class TestUrls(TestCase):

    def setUp(self):
        mock_image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        # Set up a user for authentication tests
        self.user = User.objects.create_user(username='testuser', email='user@example.com', password='testpass123')
        self.client.login(username='testuser', password='testpass123')
        self.item = Item.objects.create(itemType='Mouse', itemDescription='A wireless mouse', itemPrice=10.00,
                                        itemQuantity=5, itemImage=mock_image)

    def test_index_url_resolves(self):
        path = reverse('index')
        self.assertEqual(resolve(path).func, views.index)

    def test_payment_url_resolves(self):
        path = reverse('payment', args=[1])
        self.assertEqual(resolve(path).func, views.payment)

    def test_pay_url_resolves(self):
        path = reverse('pay', args=[1])
        self.assertEqual(resolve(path).func, views.pay)

    def test_about_url_resolves(self):
        path = reverse('about')
        self.assertEqual(resolve(path).func, views.render_about_page)

    def test_contact_url_resolves(self):
        path = reverse('contact')
        self.assertEqual(resolve(path).func, views.render_contact_page)

    def test_registration_url_resolves(self):
        path = reverse('registration')
        self.assertEqual(resolve(path).func, views.render_registration_page)

    def test_validateUser_url_resolves(self):
        path = reverse('validateUser')
        self.assertEqual(resolve(path).func, forms.validate_registration_details)

    def test_login_url_resolves(self):
        path = reverse('log')
        self.assertEqual(resolve(path).func, views.login_view)

    def test_authenticate_url_resolves(self):
        path = reverse('authenticate')
        self.assertEqual(resolve(path).func, forms.authenticate_user)

    def test_logout_url_resolves(self):
        path = reverse('logout')
        self.assertEqual(resolve(path).func, views.logout_view)

    def test_account_url_redirects_when_not_logged_in(self):
        self.client.logout()  # Ensure the user is logged out
        path = reverse('account')
        response = self.client.get(path, secure=True)
        self.assertEqual(response.status_code, 302)

    def test_valid_payment_url(self):
        path = reverse('payment', kwargs={'item_id': 1})
        response = self.client.get(path, secure=True)
        self.assertEqual(response.status_code, 200)

    def test_invalid_payment_url(self):
        with self.assertRaises(NoReverseMatch):
            path = reverse('payment', kwargs={'item_id': 999999})
            # If the test reaches this line, it means the reverse call did not raise an exception,
            # hence, the test will fail. If an exception is raised, the test will pass.
            self.client.get(path, secure=True)

    def test_secure_page_access_without_login(self):
        self.client.logout()
        secure_pages = [reverse('account'), reverse('logout')]
        for page in secure_pages:
            response = self.client.get(page)
            self.assertTrue(response.status_code, 302)  # Redirect or Unauthorized

    def tearDown(self):
        self.user.delete()
