from django.test import TestCase
from products.models import Product, Category
from django.urls import reverse


class ProductTest(TestCase):

    def test_product_list_view_get(self):
        response = self.client.get(reverse('products:products_list', kwargs={'slug':"slug1/"}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'products/product_list.html')
        self.failUnless(isinstance(response.context['category'], Category))
        self.failUnless(isinstance(response.context['categories'], Category))
        self.failUnless(isinstance(response.context['products'], Product))

"""
def product_list(request, slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if slug:
        category = get_object_or_404(Category, slug=slug)
        products = Product.objects.filter(category=category)

    context = {
            'category' : category,
            'categories' : categories,
            'products' : products
        }
    return render(request, 'products/product_list.html', context)

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    context = {
            'product' : product,
            'cart_product_form': cart_product_form

    }
    return render(request, 'products/product_detail.html', context)
"""