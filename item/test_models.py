from django.test import TestCase
from django.contrib.auth.models import User

from item.models import Item, History


class ItemModelTest(TestCase):

    def setUp(self):
        self.item = Item.objects.create(
            itemType='Mouse',
            itemDescription='A wireless mouse',
            itemPrice=10.00,
            itemQuantity=5
        )

    def test_delete_one_item(self):
        self.assertTrue(self.item.dispenseOneItem(False))
        self.assertEqual(self.item.itemQuantity, 4)

    def test_add_quantity(self):
        self.item.addQuantity(3)
        self.assertEqual(self.item.itemQuantity, 8)

    def test_empty(self):
        self.item.empty()
        self.assertEqual(self.item.itemQuantity, 0)

class HistoryModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.history = History.objects.create(
            user=self.user,
            hItemType='Mouse',
            hItemPrice=10.00
        )

    def test_clean(self):
        self.history.clean()
        self.assertFalse(History.objects.filter(id=self.history.id).exists())

