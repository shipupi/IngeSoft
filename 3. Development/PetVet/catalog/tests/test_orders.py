from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from decimal import Decimal
import datetime

from orders import urls
from orders import forms
from orders.models import OrderItem, Order
from orders.forms import OrderCreateForm
from cart.cart import Cart
from products.models import Product, Category


valid_form_data = [{'first_name':'Test1', 'last_name':'User1','email':'tu1@gmail.com', 'address':'somewhere', 'postal_code':'12', 'city':'BA', 'created':datetime.datetime.now(), 'cc_number':'4925590926750799','cc_expiry':'01/2020','cc_code':'010','paid':True},
		           {'first_name':'Test2', 'last_name':'User2','email':'tu2@yahoo.com', 'address':'out', 'postal_code':'12', 'city':'BA', 'cc_number':'5414331598041802', 'cc_expiry':'12/2025','cc_code':'199'},
		           {'first_name':'Test3', 'last_name':'User3','email':'tu3@hotmail.com', 'address':'there', 'postal_code':'34', 'city':'London', 'cc_number':'6011204893370744','cc_expiry':'02/2021', 'cc_code':'120'}
                  ]

invalid_form_data = [{'first_name':'Test1', 'last_name':'User1','email':'tu1', 'address':'somewhere', 'postal_code':'12', 'city':'BA', 'created':datetime.datetime.now(), 'cc_number':'4925590926750790','cc_expiry':'01/2020','cc_code':'010','paid':True},
	     	         {'first_name':'Really long name that will exceed the 60 maximum characters. Just a little more!', 'last_name':'User2','email':'tu2@yahoo.com', 'address':'out', 'postal_code':'12', 'city':'BA', 'cc_expiry':'12/2005'},
		             {'first_name':'Test3', 'last_name':'User3','email':'tu3@hotmail.com', 'address':'there', 'postal_code':'34', 'city':'London', 'cc_number':'0000000000000000'},
                     {'first_name':'Test3', 'last_name':'User3','email':'tu3@hotmail.com', 'address':'there', 'postal_code':'34', 'city':'London', 'cc_number':'6011204893370744', 'cc_expiry':'01/2001'}]


#----------------------------- ORDER FORM -------------------------------#

class OrderCreateFormTest(TestCase):
    """
    Form should be valid when restrictions are followed
    """
    def test_order_create_form_valid(self):
        for data in valid_form_data:
            form = OrderCreateForm(data)
            self.assertTrue(form.is_valid())

    """
    Form should be invalid when any restriction is not followed
    """
    def test_order_create_form_invalid(self):
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
        cls.test_cart = Cart(cls.request)

        #Creating the products
        category = Category.objects.create(name='C1', slug='c1')
        cls.product1 = Product.objects.create(name="Prod1", slug="p1", description='', price=Decimal("100"), available=True, stock=1, created_at=datetime.datetime.now())
        cls.product2 = Product.objects.create(name="Prod2", slug="p2", description='', price=Decimal("100"), available=True, stock=1, created_at=datetime.datetime.now())
        cls.product1.categories.add(category)
        cls.product2.categories.add(category)
       
        # Adding products to the cart
        #cls.test_cart.add(cls.product1, quantity=1)
        #cls.test_cartt.add(cls.product2, quantity=2)
        cls.order = Order.objects.create()
        cls.order_item_1 = OrderItem.objects.create(order=cls.order, product=cls.product1, price=cls.product1.price, quantity=1)
        cls.order_item_2 = OrderItem.objects.create(order=cls.order, product=cls.product2, price=cls.product2.price, quantity=1)

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
    A POST to the create_order view with invalid form data
    populates the OrderCreateForm into context in 'form'.
    """
    def test_order_create_view_invalid_form_post(self):
    	for invalid_data in invalid_form_data:
    	    response = self.client.post(reverse('orders:order_create'), invalid_data)
    	    self.assertEqual(response.status_code, 200)
    	    self.failUnless(isinstance(response.context['form'], forms.OrderCreateForm))

    """  """
    def test_proper_redirects_to_order_create(self):
    	data = valid_form_data[0]
    	response = self.client.post(reverse('orders:order_create'), data)	
    	self.assertEqual(response.status_code, 200)

    def test_order_items_created_on_valid_form(self):
    	# There were two products in the cart, checking if both OrderItem were created properly
    	self.assertEqual(OrderItem.objects.count(), 2)
    	self.assertTrue(OrderItem.objects.filter(product=self.product1).exists())  #Returns True if the QuerySet is not empty
    	self.assertTrue(OrderItem.objects.filter(product=self.product2).exists())  #Returns True if the QuerySet is not empty
    
    def test_order_contains_created_order_items(self):
        self.assertTrue(self.order_item_1.order==self.order)
        self.assertTrue(self.order_item_2.order==self.order)
