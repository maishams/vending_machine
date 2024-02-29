# Import necessary Django modules
from django.db import models
from django.db.models import F
from django.utils import timezone
from django.contrib.auth.models import User

# Constants for Different Equipment Types
EQUIPMENT_TYPES = [
    'Keyboard', 'Mouse', 'Headphones', 'USB Drive', 'Laptop Charger',
    'HDMI Cable', 'Ethernet Cable', 'Wireless Adapter', 'Web Camera',
    'Microphone', 'Power Bank', 'Phone Charger'
]

# Convert the equipment types into a format suitable for Django model choices
ITEM_CHOICES = tuple((item, item) for item in EQUIPMENT_TYPES)


def get_item_choices():
    """Utility function to retrieve item choices."""
    return ITEM_CHOICES


class Item(models.Model):
    """Model representing each equipment item in the vending machine."""

    itemType = models.CharField(
        'Type', choices=ITEM_CHOICES, max_length=25, default='Mouse'
    )
    itemDescription = models.TextField(
        'Description', max_length=400, help_text="Insert a brief product description", default=""
    )
    itemPrice = models.DecimalField(
        'Price', max_digits=4, decimal_places=2, default=0
    )
    itemQuantity = models.PositiveSmallIntegerField(
        'Quantity', default=1, editable=True
    )
    itemImage = models.ImageField(blank=True, null=True)

    def __str__(self):
        """String representation of the model instance."""
        return str(self.itemType)

    def dispense_one_item(self, is_last):
        """Method to decrease the quantity of an item by 1."""
        if self.itemQuantity > 0:
            self.itemQuantity -= 1
            self.save()
            return self.itemQuantity == 0 if is_last else True
        else:
            raise ValueError

    def add_quantity(self, number):
        """Method to add a specified quantity to the item."""
        if number > 0:
            Item.objects.filter(id=self.id).update(itemQuantity=F('itemQuantity') + number)
            self.refresh_from_db()
        else:
            raise ValueError

    def empty(self):
        """Method to set the item quantity to 0."""
        Item.objects.filter(id=self.id).update(itemQuantity=0)
        self.refresh_from_db()


class History(models.Model):
    """Model to keep track of equipment purchase history for each user."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hItemType = models.CharField(
        'Type', choices=ITEM_CHOICES, max_length=25
    )
    hItemPrice = models.DecimalField(
        'Price', max_digits=4, decimal_places=2, default=0.50
    )
    purchaseTime = models.DateTimeField(
        'Purchase Time', default=timezone.now
    )

    def clean(self):
        """Method to delete a history record."""
        self.delete()
