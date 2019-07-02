from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from decimal import Decimal
import datetime

from orders import urls
from orders import forms
from cart.cart import Cart
from products.models import Product, Category

valid_form_data = [{'first_name':'Test1', 'last_name':'User1','email':'tu1@gmail.com', 'address':'somewhere', 'postal_code':'12', 'city':'BA', 'created':datetime.datetime.now(), 'cc_number':'1111111111000000','cc_expiry':'01/2020','cc_code':'010','paid':True},
		   {'first_name':'Test2', 'last_name':'User2','email':'tu2@yahoo.com', 'address':'out', 'postal_code':'12', 'city':'BA', 'cc_expiry':'12/2005'},
		   {'first_name':'Test3', 'last_name':'User3','email':'tu3@hotmail.com', 'address':'there', 'postal_code':'34', 'city':'London', 'cc_number':'1234567890123456'}]

invalid_form_data = [{'first_name':'Test1', 'last_name':'User1','email':'tu1', 'address':'somewhere', 'postal_code':'12', 'city':'BA', 'created':datetime.datetime.now(), 'cc_number':'1111111111000000','cc_expiry':'01/2020','cc_code':'010','paid':True},
	     	     {'first_name':'Really long name that will exceed the 60 maximum characters. Just a little more!', 'last_name':'User2','email':'tu2@yahoo.com', 'address':'out', 'postal_code':'12', 'city':'BA', 'cc_expiry':'12/2005'},
		     {'first_name':'Test3', 'last_name':'User3','email':'tu3@hotmail.com', 'address':'there', 'postal_code':'34', 'city':'London', 'cc_number':'-234567890$123456'}]


#----------------------------- ORDER FORM -------------------------------#

class OrderCreateFormTest(TestCase):
    """
    Form should be valid when restrictions are followed
    """
    def test_cart_add_product_form_valid(self):
        for data in valid_form_data:
            form = OrderCreateForm(data)
            self.assertTrue(form.is_valid())

    """
    Form should be invalid when any restriction is not followed
    """
    def test_cart_add_product_form_invalid(self):
        for data in invalid_form_data:
            form = OrderCreateForm(data)
            self.assertFalse(form.is_valid())


#----------------------------- ORDER VIEW -------------------------------#

class OrdersViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
    	# Creating a cart
    	cls.request = RequestFactory()
    	cls.request.user = AnonymousUser()
    	cls.request.session ={}
    	cls.cartObj = Cart(cls.request)
    	# Creating products
    	category = Category.objects.create(name='C1', slug='c1')
    	cls.product1 = Product.objects.create(category=category, name="Prod1", slug="p1", description='', price=Decimal("100"), available=True, stock=1, created_at=datetime.datetime.now())
    	cls.product2 = Product.objects.create(category=category, name="Prod2", slug="p2", description='', price=Decimal("100"), available=True, stock=1, created_at=datetime.datetime.now())
    	# Adding products to the cart
    	cls.cartObj.add(product1, quantity=1)
    	cls.cartObj.add(product2, quantity=2)


    def setUp(self):
    	self.client = Client()

    """
    A GET to the create_order view uses the appropriate
    template and populates the OrderCreateForm into context in 'form'.
    """
    def test_order_create_view_get(self):
    	response = self.client.get(reverse('orders:order_create'),request=self.request)
    	self.assertEqual(response.status_code, 200)
    	self.assertTemplateUsed(response,'orders/form.html')
    	self.failUnless(isinstance(response.context['form'], forms.OrderCreateForm))

    """
    A POST to the create_order view with valid form data
    populates the OrderCreateForm into context in 'order'.
    """
    def test_order_create_view_valid_form_post(self):
    	print("ERROR because the form isnt valid when it should be")

    	for valid_data in valid_form_data:
    	    response = self.client.post(reverse('orders:order_create'), valid_data)
    	    self.assertEqual(response.status_code, 200)
    	    self.failUnless(isinstance(response.context['order'], forms.OrderCreateForm))

    """
    A POST to the create_order view with invalid form data
    populates the OrderCreateForm into context in 'form'.
    """
    def test_order_create_view_invalid_form_post(self):
    	for invalid_data in invalid_form_data:
    	    response = self.client.post(reverse('orders:order_create'), invalid_data)
    	    self.assertEqual(response.status_code, 200)
    	    self.failUnless(isinstance(response.context['form'], forms.OrderCreateForm))


    """ NO SE COMO PASARLE EL REQUEST QUE CREE EN setUpTestData PORQUE ESE CONTIENE EL CART CON LAS COSAS
        ENTONCES AL TENER LA MISMA SECCION ME VA A DEVOLVER ESE MISMO CARRITO """

    def test_order_items_created_on_valid_form(self):
    	data = valid_form_data[0]
    	response = self.client.post(reverse('orders:order_create'), data)	
    	self.assertEqual(response.status_code, 200)

    	# There were two products in the cart, checking if both where created into OrderItem
    	self.assertEqual(OrderItem.objects.count(), 2)
    	self.assertTrue(OrderItem.objects.filter(product=cls.product1).exists())  #Returns True if the QuerySet is not empty
    	self.assertTrue(OrderItem.objects.filter(product=cls.product2).exists())  #Returns True if the QuerySet is not empty
