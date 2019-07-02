from django.test import TestCase, Client
from django.urls import reverse
from decimal import Decimal
import datetime

from orders import urls
from orders import forms

valid_form_data = [{'first_name':'Test1', 'last_name':'User1','email':'tu1@gmail.com', 'address':'somewhere', 'postal_code':'12', 'city':'BA', 'created':datetime.datetime.now(), 'cc_number':'1111111111000000','cc_expiry':'01/2020','cc_code':'010','paid':True},
				   {'first_name':'Test2', 'last_name':'User2','email':'tu2@yahoo.com', 'address':'out', 'postal_code':'12', 'city':'BA', 'cc_expiry':'12/2005'},
				   {'first_name':'Test3', 'last_name':'User3','email':'tu3@hotmail.com', 'address':'there', 'postal_code':'34', 'city':'London', 'cc_number':'1234567890123456'}]

invalid_form_data = [{'first_name':'Test1', 'last_name':'User1','email':'tu1', 'address':'somewhere', 'postal_code':'12', 'city':'BA', 'created':datetime.datetime.now(), 'cc_number':'1111111111000000','cc_expiry':'01/2020','cc_code':'010','paid':True},
				     {'first_name':'Really long name that will exceed the 60 maximum characters. Just a little more!', 'last_name':'User2','email':'tu2@yahoo.com', 'address':'out', 'postal_code':'12', 'city':'BA', 'cc_expiry':'12/2005'},
				     {'first_name':'Test3', 'last_name':'User3','email':'tu3@hotmail.com', 'address':'there', 'postal_code':'34', 'city':'London', 'cc_number':'-234567890$123456'}]




class OrdersViewTest(TestCase):
	def setUp(self):
		self.client = Client()

	def test_order_create_view_get(self):
		response = self.client.get(reverse('orders:order_create'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response,'orders/form.html')
		self.failUnless(isinstance(response.context['form'], forms.OrderCreateForm))

	def test_order_create_view_valid_form_post(self):
		for valid_data in valid_form_data:
			response = self.client.post(reverse('orders:order_create'), valid_data)
			self.assertEqual(response.status_code, 200)
			self.failUnless(isinstance(response.context['order'], forms.OrderCreateForm))




