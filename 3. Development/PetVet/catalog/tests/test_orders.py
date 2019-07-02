from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from decimal import Decimal
import datetime
from django.conf import settings
from importlib import import_module

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
        #Creating the products
        category = Category.objects.create(name='C1', slug='c1')
        cls.product1 = Product.objects.create(name="Prod1", slug="p1", description='', price=Decimal("100"), available=True, stock=1, created_at=datetime.datetime.now())
        cls.product2 = Product.objects.create(name="Prod2", slug="p2", description='', price=Decimal("200"), available=True, stock=1, created_at=datetime.datetime.now())
        cls.product1.categories.add(category)
        cls.product2.categories.add(category)
        

    def setUp(self):

        self.client = Client()
        
        settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        self.session = store
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key

        # Creating a request to create the cart
        request = RequestFactory()
        request.user = AnonymousUser()
        request.session = {}
        self.test_cart = Cart(request)

        # Adding products to the cart
        self.test_cart.add(self.product1, quantity=1)
        self.test_cart.add(self.product2, quantity=2)

        # Making the client session hold the cart as well
        s = self.session
        s[settings.CART_SESSION_ID] = self.test_cart.cart
        s.save()
        print(self.client.session[settings.CART_SESSION_ID])


    """
    A GET to the create_order view uses the appropriate
    template and populates the OrderCreateForm into context in 'form'.
    """
    def test_order_create_view_get(self):
    	response = self.client.get(reverse('orders:order_create'))
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

    """  
    A POST of valid data with a non empty cart creates the correct OrderItem
    based on the products that reside in the cart. In this case, product 1 and 2
    """
    def test_order_items_created_on_valid_form(self):
        data = valid_form_data[0]
        response = self.client.post(reverse('orders:order_create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(OrderItem.objects.count(), 2)
        self.assertTrue(OrderItem.objects.filter(product=self.product1).exists())  #Returns True if the QuerySet is not empty
        self.assertTrue(OrderItem.objects.filter(product=self.product2).exists())  #Returns True if the QuerySet is not empty

    """  
    Will check that if I create a form with the same data I pass to the create_order view, the orderItem order coincides with the form
    Checks both orderItems created hold the same information as the products in the cart
    """
    def test_correct_data_in_order_items(self):
        data = valid_form_data[0]
        form = OrderCreateForm(data).save()

        response = self.client.post(reverse('orders:order_create'), data)
        self.assertEqual(response.status_code, 200)

        orderItem1 = OrderItem.objects.get(product=self.product1)
        orderItem2 = OrderItem.objects.get(product=self.product2)

        # Verifying orderItem1
        self.assertTrue(orderItem1.order.first_name == form.first_name)
        self.assertTrue(orderItem1.order.last_name == form.last_name)
        self.assertTrue(orderItem1.order.email == form.email)
        self.assertTrue(orderItem1.order.address == form.address)
        self.assertTrue(orderItem1.order.city == form.city)
        self.assertTrue(orderItem1.order.postal_code == form.postal_code)
        self.assertTrue(orderItem1.order.cc_number == form.cc_number)
        self.assertTrue(orderItem1.order.cc_expiry == form.cc_expiry)
        self.assertTrue(orderItem1.order.cc_code == form.cc_code)
        self.assertTrue(orderItem1.order.paid == form.paid)

        self.assertTrue(orderItem1.product == self.product1)
        self.assertTrue(orderItem1.price == Decimal("100"))
        self.assertTrue(orderItem1.quantity == 1)
        
        # Verifying orderItem2
        self.assertEqual(orderItem2.order, orderItem1.order)
        self.assertTrue(orderItem2.product == self.product2)
        self.assertTrue(orderItem2.price == Decimal("200"))
        self.assertTrue(orderItem2.quantity == 2)
