import os
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.test import TestCase
from django.urls import reverse

import datetime
from decimal import Decimal
from products import urls
from products.models import Product, Category

class ProductTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name='C1', slug='c1')
        cls.category2 = Category.objects.create(name='C2', slug='c2')

    def setUp(self):
        img_path = os.path.join(settings.BASE_DIR, 'static/images/item-01.jpg')
        test_photo = SimpleUploadedFile(name='test_image.jpg', content=open(img_path, 'rb').read(), content_type='image/jpeg')
        
        self.product1 = Product.objects.create(name="Prod1", slug="p1", description='', price=Decimal("100"), available=True, stock=1, created_at=datetime.datetime.now(), image=test_photo)
        self.product2 = Product.objects.create(name="Prod2", slug="p2", description='', price=Decimal("100"), available=True, stock=1, created_at=datetime.datetime.now(), image=test_photo)
        self.product1.categories.add(self.category)
        self.product2.categories.add(self.category)

    """
    A GET to the product list view with no slug uses the appropriate
    template and populates the context with the correct information.
    """
    def test_product_list_no_slug_view_get(self):
        response = self.client.get(reverse('products:products_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'products/product_list.html')
        self.assertEqual(response.context['category'], None)
        self.assertEqual(list(response.context['categories']), list(Category.objects.all()))
        self.assertEqual(list(response.context['products']), list(Product.objects.filter(available=True)))

    """
    A GET to the product list view with an existing category slug uses the appropriate
    template and populates the context with the correct information.
    """
    def test_product_list_view_with_existing_slug_get(self):
        response = self.client.get(reverse('products:product_list_by_category', kwargs={'slug':self.category.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'products/product_list.html')
        self.failUnless(isinstance(response.context['category'], Category))
        self.assertEqual(list(response.context['categories']), list(Category.objects.all()))
        self.assertEqual(list(response.context['products']), list(Product.objects.filter(categories=response.context['category'])))

    """
    A GET to the product list view with an existing category slug which was never used on a product
    returns an empty queryset in products. Also testing that it uses the correct template
    """
    def test_empty_product_list_by_category_view_get(self):
        response = self.client.get(reverse('products:product_list_by_category', kwargs={'slug':self.category2.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'products/product_list.html')
        self.assertEqual(list(response.context['products']), [])

    """
    A GET to the product list view with a non-existing category slug returns the 404 response
    """
    def test_product_list_view_with_nonexisting_slug_get_404(self):
        response = self.client.get(reverse('products:product_list_by_category', kwargs={'slug':'Not-a-category-slug'}))
        self.assertEqual(response.status_code, 404)
       
    """
    A GET to the product detail view uses the appropriate template
    """
    def test_existing_product_detail_view_get(self):
        response = self.client.get(reverse('products:product_detail', kwargs={'id':self.product1.id, 'slug':self.product1.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'products/product_detail.html')

    """
    A GET to the product detail view of a non existing product returns 404 in the response
    """
    def test_product_detail_view_get_404(self):
        # Incorrect id
        response = self.client.get(reverse('products:product_detail', kwargs={'id':0, 'slug':self.product1.slug}))
        self.assertEqual(response.status_code, 404)
        
        # Incorrect slug
        response = self.client.get(reverse('products:product_detail', kwargs={'id':self.product1.id, 'slug':'incorrect-slug'}))
        self.assertEqual(response.status_code, 404)
