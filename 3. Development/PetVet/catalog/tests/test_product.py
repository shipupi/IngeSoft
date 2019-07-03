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
        cls.category3 = Category.objects.create(name='C3', slug='c3')
        cls.category4 = Category.objects.create(name='Cat4', slug='C4')

    def setUp(self):
        img_path = os.path.join(settings.BASE_DIR, 'static/images/item-01.jpg')
        test_photo = SimpleUploadedFile(name='test_image.jpg', content=open(img_path, 'rb').read(), content_type='image/jpeg')
        
        self.product1 = Product.objects.create(name="Prod1", slug="p1", description='', price=Decimal("100"), available=True, stock=1, created_at=datetime.datetime.now(), image=test_photo)
        self.product2 = Product.objects.create(name="Prod2", slug="p2", description='', price=Decimal("500"), available=True, stock=1, created_at=datetime.datetime.now(), image=test_photo)
        self.product3 = Product.objects.create(name="Another", slug="p3", description='', price=Decimal("600"), available=True, stock=1, created_at=datetime.datetime.now(), image=test_photo)
        self.product1.categories.add(self.category)
        self.product2.categories.add(self.category)
        self.product2.categories.add(self.category3)
        self.product3.categories.add(self.category4)

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
    def test_product_list_view_with_category3_slug_get(self):
        expectedList = []
        expectedList.insert(0, self.product2)

        response = self.client.get(reverse('products:product_list_by_category', kwargs={'slug':self.category3.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'products/product_list.html')
        self.failUnless(isinstance(response.context['category'], Category))
        self.assertEqual(list(response.context['categories']), list(Category.objects.all()))
        self.assertEqual(list(response.context['products']), expectedList)

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


    """
    Testing the product listing with no slug and price interval between 220 to 1000
    Expected result --> product2 and product3
    """
    def test_product_list_interval_220_to_1000_no_slug(self):
        expectedList = []
        expectedList.insert(0, self.product2)
        expectedList.insert(1, self.product3)

        data = {
            'price_min': Decimal("220"),
            'price_max': Decimal("1000")
        }
        response = self.client.get(reverse('products:products_list'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['products']), expectedList)

    """
    Testing the product listing with no slug and price interval between 10 to 100
    Expected result --> only product1
    """
    def test_product_list_interval_10_to_100_no_slug(self):
        expectedList = []
        expectedList.insert(0, self.product1)

        data = {
            'price_min': Decimal("10"),
            'price_max': Decimal("100")
        }
        response = self.client.get(reverse('products:products_list'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['products']), expectedList)

    """
    Testing the product listing with no slug and price interval between 200 to 400
    Expected result --> empty
    """
    def test_product_list_interval_200_to_400_no_slug(self):
        data = {
            'price_min': Decimal("200"),
            'price_max': Decimal("400")
        }
        response = self.client.get(reverse('products:products_list'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['products']), [])

    """
    Testing the product listing with category slug and price interval between 50 to 550
    Expected result --> product1 and product2. Both are in said category and between said price
    """
    def test_product_list_interval_50_to_550_with_category_slug(self):
        expectedList = []
        expectedList.insert(0, self.product1)
        expectedList.insert(1, self.product2)

        data = {
            'price_min': Decimal("50"),
            'price_max': Decimal("550"),
        }
        response = self.client.get(reverse('products:product_list_by_category', kwargs={'slug': self.category.slug}), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['products']), expectedList)

    """
    Testing the product listing with category3 slug and price interval between 50 to 550
    Expected result --> only product2. It is the only product in that category with said price
    """
    def test_product_list_interval_50_to_550_with_category3_slug(self):
        expectedList = []
        expectedList.insert(0, self.product2)

        data = {
            'price_min': Decimal("50"),
            'price_max': Decimal("550"),
        }
        response = self.client.get(reverse('products:product_list_by_category', kwargs={'slug': self.category3.slug}), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['products']), expectedList)

    """
    Testing the product listing with category3 slug and price interval between 0 to 200
    Expected result --> empty. No products with said category and price
    """    
    def test_product_list_interval_0_to_200_with_category3_slug(self):
        data = {
            'price_min': Decimal("0"),
            'price_max': Decimal("200"),
        }
        response = self.client.get(reverse('products:product_list_by_category', kwargs={'slug': self.category3.slug}), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['products']), [])

    
    def test_product_list_interval_100_to_700_search_prod_no_slug(self):
        expectedList = []
        expectedList.insert(0, self.product1)
        expectedList.insert(1, self.product2)

        data = {
            'price_min': Decimal("100"),
            'price_max': Decimal("700"),
            'search': "Prod"
        }
        response = self.client.get(reverse('products:products_list'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['products']), expectedList)
