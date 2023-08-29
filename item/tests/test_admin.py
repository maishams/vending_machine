from django.test import TestCase
from django.contrib.admin.sites import AdminSite

from item.admin import add10, add100, emptyitems, InsertItemAdmin, InsertHistoryAdmin
from item.models import Item, History


class MockRequest:
    pass


class MockSuperUser:
    def has_perm(self):
        return True


request = MockRequest()
request.user = MockSuperUser()


class TestAdminActions(TestCase):
    def setUp(self):
        # Create some test items
        self.item1 = Item.objects.create(itemType="Type1", itemQuantity=5)
        self.item2 = Item.objects.create(itemType="Type2", itemQuantity=15)

    def test_add10_action(self):
        queryset = Item.objects.all()
        add10(None, request, queryset)
        self.item1.refresh_from_db()
        self.item2.refresh_from_db()
        self.assertEqual(self.item1.itemQuantity, 15)
        self.assertEqual(self.item2.itemQuantity, 25)

    def test_add100_action(self):
        queryset = Item.objects.all()
        add100(None, request, queryset)
        self.item1.refresh_from_db()
        self.item2.refresh_from_db()
        self.assertEqual(self.item1.itemQuantity, 105)
        self.assertEqual(self.item2.itemQuantity, 115)

    def test_emptyitems_action(self):
        queryset = Item.objects.all()
        emptyitems(None, request, queryset)
        self.item1.refresh_from_db()
        self.item2.refresh_from_db()
        self.assertEqual(self.item1.itemQuantity, 0)
        self.assertEqual(self.item2.itemQuantity, 0)


class TestInsertItemAdmin(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.item_admin = InsertItemAdmin(Item, self.site)

    def test_list_display(self):
        self.assertEqual(list(self.item_admin.list_display),
                         ['id', 'itemType', 'itemDescription', 'itemPrice', 'itemQuantity'])

    def test_list_filter(self):
        self.assertEqual(list(self.item_admin.list_filter), ['itemType'])

    def test_search_fields(self):
        self.assertEqual(list(self.item_admin.search_fields), ['itemType', 'itemDescription'])

    def test_ordering(self):
        self.assertEqual(list(self.item_admin.ordering), ['id'])

    def test_actions(self):
        self.assertIn(add10, self.item_admin.actions)
        self.assertIn(add100, self.item_admin.actions)
        self.assertIn(emptyitems, self.item_admin.actions)


class TestInsertHistoryAdmin(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.history_admin = InsertHistoryAdmin(History, self.site)

    def test_list_display(self):
        self.assertEqual(list(self.history_admin.list_display), ['user', 'hItemType', 'hItemPrice', 'purchaseTime'])

    def test_list_filter(self):
        self.assertEqual(list(self.history_admin.list_filter), ['hItemType', 'purchaseTime'])

    def test_search_fields(self):
        self.assertEqual(list(self.history_admin.search_fields), ['user', 'hItemType'])

    def test_ordering(self):
        self.assertEqual(list(self.history_admin.ordering), ['-purchaseTime'])
