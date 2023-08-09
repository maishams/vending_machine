# Import necessary Django modules
from django.db import models
from django.db.models import F
from django.utils import timezone
from django.contrib.auth.models import User

# Define constants for different types of equipment items
# These constants will be used to populate the choices for the equipment type field in the model
ITEM_CHOICES = ((name, name) for name in (
    'Keyboard',
    'Mouse',
    'Headphones',
    'USB Drive',
    'Laptop Charger',
    'HDMI Cable',
    'Ethernet Cable',
    'Wireless Adapter',
    'Web Camera',
    'Microphone',
    'Power Bank',
    'Phone Charger'
))

# Method to get item choice tuple
def getItemChoices():
    return ITEM_CHOICES


# Define the Item model to represent each equipment item in the vending machine
class Item(models.Model):
    itemType = models.CharField('Type', choices=ITEM_CHOICES, max_length=25, default="Mouse")
    itemDescription = models.TextField('Description', max_length=400, help_text="Insert a brief product description",
                                       default="")
    itemPrice = models.DecimalField('Price', max_digits=4, decimal_places=2, default=0.50)
    itemQuantity = models.PositiveSmallIntegerField('Quantity', default=1, editable=True)
    itemImage = models.ImageField(blank=True, null=True)

    # String representation of the model instance
    def __str__(self):
        return str(self.itemType)

    # Method to decrease the quantity of an item by 1
    def dispenseOneItem(self, isLast):
        # If there's no item left, delete the record
        if self.itemQuantity == 0:
            self.delete()
            return False

        # If there's only one item left
        if self.itemQuantity == 1:
            # If it's the last item and isLast is True, set quantity to 0
            if isLast:
                self.itemQuantity = 0
                self.save()
            # If it's not the last item or isLast is False, delete the record
            else:
                self.delete()
            return True

        # If there's more than one item, decrease the quantity by 1
        if self.itemQuantity > 1:
            self.itemQuantity -= 1
            self.save()
            return True

        # If none of the above conditions are met, return False
        return False

    # Method to add a specified quantity to the item
    def addQuantity(self, number):
        Item.objects.filter(id=self.id).update(itemQuantity=F('itemQuantity') + number)
        Item.refresh_from_db(self)

    # Method to set the item quantity to 0
    def empty(self):
        Item.objects.filter(id=self.id).update(itemQuantity=0)
        Item.refresh_from_db(self)


# Define the History model to keep track of equipment purchase history for each user
class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user who made the purchase
    hItemType = models.CharField('Type', choices=ITEM_CHOICES, max_length=25)
    hItemPrice = models.DecimalField('Price', max_digits=4, decimal_places=2, default=0.50)
    purchaseTime = models.DateTimeField('Purchase Time', default=timezone.now)  # Timestamp of the purchase

    # Method to delete a history record
    def clean(self):
        self.delete()