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

    def test_dispense_reduces_quantity_by_one(self):
        self.assertTrue(self.item.dispense_one_item(False))
        self.assertEqual(self.item.itemQuantity, 4)

    def test_dispense_sets_quantity_to_zero_when_one_remaining(self):
        # Setting Item Quantity For Test
        self.item.itemQuantity = 1

        self.item.dispense_one_item(True)
        self.assertEqual(self.item.itemQuantity, 0)

    def test_dispense_raises_error_at_zero_quantity(self):
        # Setting Item Quantity For Test
        self.item.itemQuantity = 0

        with self.assertRaises(ValueError):
            self.item.dispense_one_item(True)

    def test_add_quantity_increases_quantity_correctly(self):
        self.item.add_quantity(3)
        self.assertEqual(self.item.itemQuantity, 8)

    def test_add_negative_quantity_raises_error(self):
        # Setting Item Quantity For Test
        self.item.itemQuantity = 5

        with self.assertRaises(ValueError):
            self.item.add_quantity(-5)

    def test_empty_sets_quantity_to_zero(self):
        self.item.empty()
        self.assertEqual(self.item.itemQuantity, 0)


class HistoryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.history = History.objects.create(
            user=self.user,
            hItemType='Item1',
            hItemPrice=10.00
        )

    def test_history_clean_deletes_record(self):
        self.history.clean()
        self.assertFalse(History.objects.filter(id=self.history.id).exists())

    def test_clean_history_does_not_affect_others(self):
        # Setup for another History object
        user2 = User.objects.create(username="testuser2", password='12345')
        history_to_delete1 = History.objects.create(user=user2, hItemType="Item2", hItemPrice=20.00)

        history_to_delete1.clean()
        self.assertEqual(History.objects.count(), 1)
