import os
import datetime

from django.conf import settings
from django.contrib.auth.models import User, AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse

from cart import urls
from cart.cart import Cart
from cart.forms import CartAddProductForm
from decimal import Decimal
from products.models import Product, Category

class CartWithProductTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="Things", slug="things")
    
    def setUp(self):
        self.request = RequestFactory()
        self.request.user = AnonymousUser()
        self.request.session ={}
        self.cartObj = Cart(self.request)

    """
    Newly created cart in a new session should be empty
    """
    def test_cart_is_empty(self):
        self.assertEqual(self.cartObj.cart, {})
    
    """
    Auxiliary function that creates a cart with a new request but the 
    same session as in the setUp(self)function
    """
    def create_cart_in_same_session(self):
        newRequest = RequestFactory()
        newRequest.session = self.request.session
        newRequest.user = self.request.user

        return Cart(newRequest)

    """
    Functions to test that the same cart is returned with the same session
    whether its empty or has loaded products
    """
    def test_same_session_same_cart_empty(self):
        newCart = self.create_cart_in_same_session()
        self.assertEqual(newCart.cart, self.cartObj.cart)

    def test_same_session_same_cart_with_products(self):
        self.cartObj.cart["0"] = {'quantity': 2, 'price': str(100)} 
        self.cartObj.cart["1"] = {'quantity': 3, 'price': str(200)} 
        self.cartObj.cart["2"] = {'quantity': 8, 'price': str(12)} 
        self.cartObj.cart["3"] = {'quantity': 10, 'price': str(1023)} 

        newCart = self.create_cart_in_same_session()
        self.assertEqual(newCart.cart, self.cartObj.cart)

    """
    Auxiliary function that creates a product
    """
    def create_product(self, name, slug, price=Decimal("100"), stock=5, 
        created_at=datetime.datetime.now()):

        product = Product.objects.create(name=name, slug=slug, description='', price=price, available=True, stock=stock, created_at=created_at)
        product.categories.add(self.category)

        return product

    """
    Testing that the cart adds new products correctly and that the iter 
    can iterate through these said products correctly
    """
    def test_cart_add_new_product_and_iter(self):
        product1 = self.create_product(name="First product", slug="1")
        product2 = self.create_product(name="Second product", slug="2")
        self.cartObj.add(product1, quantity=1)
        self.cartObj.add(product2, quantity=2)

        # Creating the cart iter
        cartIter = iter(self.cartObj)

        # First item
        item1 = next(cartIter)
        self.assertEqual(item1['product'], product1, "First item in cart should be equal the first product we added")
        self.assertEqual(item1['price'], Decimal("100"), "Price of the first item stored in the cart should equal 100")
        self.assertEqual(item1['quantity'], 1, "The first item in cart should have 1 in it's quantity")
        
        # Second item
        item2 = next(cartIter)
        self.assertEqual(item2['product'], product2, "Second item in cart should be equal the second product we added")
        self.assertEqual(item2['price'], Decimal("100"), "Price of the second item stored in the cart should equal 100")
        self.assertEqual(item2['quantity'], 2, "The second item in cart should have 2 in it's quantity")


    """
    Test for the update quantity part of the add function
    Supposing the product.id section works properly
    """
    def test_cart_add_update_quantity(self):
        product = self.create_product(name="Update product", slug="U")
        
        self.cartObj.add(product, quantity=1)               # Adding the product for the first time to the cart
        self.cartObj.add(product, quantity=3, update_quantity=False)    # Adding quantity to the product --> should ADD to the previous one
        self.assertEqual(self.cartObj.cart[str(product.id)]['quantity'], 4)

        self.cartObj.add(product, quantity=10, update_quantity=True)    # Should update the quantity to 10
        self.assertEqual(self.cartObj.cart[str(product.id)]['quantity'], 10)

    """
    Testing the correct updating of the carts length and total price
    """
    def test_cart_update_len_and_total_price(self):
        product1 = self.create_product(name="Update cart product1", slug="U1")
        product2 = self.create_product(name="Update cart product2", slug="U2", price=Decimal("20"))

        # Cart is empty except these three products that are worth 100 each
        self.cartObj.add(product1, quantity=3)
        self.assertEqual(len(self.cartObj), 3)
        self.assertEqual(self.cartObj.get_total_price(), 300)

        # Added 7 products with value of 20 --> adding 140 to total
        self.cartObj.add(product2, quantity=7)
        self.assertEqual(len(self.cartObj), 10)
        self.assertEqual(self.cartObj.get_total_price(), 440)

        # Updating quantity of first product to 1 --> decreased the price by 200
        self.cartObj.add(product1, quantity=1, update_quantity=True)
        self.assertEqual(len(self.cartObj), 8)
        self.assertEqual(self.cartObj.get_total_price(), 240)

    """
    Testing the correct removal of a product from the cart
    """
    def test_remove_product_from_cart(self):
        product1 = self.create_product(name="To remove product1", slug="R1")
        product2 = self.create_product(name="To remove product2", slug="R2")
        self.cartObj.add(product1, quantity=1)
        self.cartObj.add(product2, quantity=1)

        self.assertEqual(len(self.cartObj), 2)

        self.cartObj.remove(product1)
        self.assertEqual(len(self.cartObj), 1)

        self.cartObj.remove(product2)
        self.assertEqual(len(self.cartObj), 0)


#--------------------------- CART FORM -----------------------------#

valid_form_data = [{'quantity':2, 'update':True},
                   {'quantity':20, 'update':''}]
                  
invalid_form_data = [{'quantity':0, 'update':True},     #Quantity cannot be 0
                     {'quantity':-10, 'update':False},  #Quantity cannot be negative
                     {'quantity':1000, 'update':''}]    #Quantity exceeds the limit


class CartAddProductFormTest(TestCase):  
    """
    Form should be valid when quantity is positive 
    and in the correct limits
    """
    def test_cart_add_product_form_valid(self):
        for data in valid_form_data:
            form = CartAddProductForm(data)
            self.assertTrue(form.is_valid())

    """
    Form should be invalid when quantity is negative/zero
    or whenr it exceeds the maximum amount
    """
    def test_cart_add_product_form_invalid(self):
        for data in invalid_form_data:
            form = CartAddProductForm(data)
            self.assertFalse(form.is_valid())


#--------------------------- CART VIEWS -----------------------------#

class CartViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="Views", slug="views")

    def setUp(self):
        self.client = Client()
        self.request = RequestFactory()
        self.request.user = AnonymousUser()
        self.request.session = {}

        img_path = os.path.join(settings.BASE_DIR, 'static/images/item-01.jpg')
        test_photo = SimpleUploadedFile(name='test_image.jpg', content=open(img_path, 'rb').read(), content_type='image/jpeg')
        
        self.product = Product.objects.create(name="Prod Name", slug="slug", description='', price=Decimal("100"), available=True, stock=1, created_at=datetime.datetime.now(), image=test_photo)
        self.product.categories.add(self.category)
    """
    A GET to the cart detail view uses the appropriate
    template and populates the Cart instance into.
    """
    def test_cart_detail_view_get(self):
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'cart/detail.html')
        self.failUnless(isinstance(response.context['cart'], Cart))

    """
    A POST to the cart add product view properly redirects.
    """
    def test_cart_add_view_redirect(self):
        response = self.client.post(reverse('cart:cart_add', kwargs={'product_id':self.product.id}), data={'quantity':10})
        self.assertRedirects(response, reverse('cart:cart_detail'))

    """
    A POST to the cart add product view with invalid product data redirects 404 status erorr page.
    """
    def test_cart_add_product_view_redirect_404(self):
        response = self.client.post(reverse('cart:cart_add', kwargs={'product_id':100}), data={'quantity':10})
        self.assertEqual(response.status_code, 404)
    
    """
    A POST to the cart remove product view properly redirects.
    """
    def test_cart_remove_product_view_redirect(self):
        response = self.client.post(reverse('cart:cart_remove', kwargs={'product_id':self.product.id}))
        self.assertRedirects(response, reverse('cart:cart_detail'))

    """
    A POST to the cart remove product view with invalid product data redirects 404 status erorr page.
    """
    def test_cart_remove_product_view_redirect_404(self):
        response = self.client.post(reverse('cart:cart_add', kwargs={'product_id':100}))
        self.assertEqual(response.status_code, 404)