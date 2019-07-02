from django.db import models
from creditcards.models import CardNumberField, CardExpiryField
from creditcards.models import SecurityCodeField
# Create your models here.
from django.contrib.auth.models import User
from products.models import Product


from django.contrib.auth import get_user_model
User = get_user_model()
class Order(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField()
    address = models.CharField(max_length=150)
    postal_code = models.CharField(max_length=30)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    cc_number = CardNumberField('card number', default='0000000000000000')
    cc_expiry = CardExpiryField('expiration date', default="01/01")
    cc_code = SecurityCodeField('security code', default ='000')
    paid = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)




    class Meta:
        ordering=('-created',)

    def __str__(self):
        return 'Order{}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_total_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items',
            on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items',
            on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
