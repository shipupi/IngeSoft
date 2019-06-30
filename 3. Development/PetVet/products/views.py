from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Product, Category
from cart.forms import CartAddProductForm

# Create your views here.

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

class CategoryList(ListView): 
	model = Category

class ProductList(ListView): 
	model = Product

class CategoryDetail(DetailView): 
	model = Category

class ProductDetail(DetailView): 
	model = Product

class CategoryCreate(CreateView): 
	model = Category
	fields = ['name']

class ProductCreate(CreateView): 
	model = Product
	fields = ['name', 'description','image','category','stock']

class CategoryUpdate(UpdateView): 
	model = Category
	fields = ['name']

class ProductUpdate(UpdateView): 
	model = Product
	fields = ['name', 'description','image','category','stock']


class CategoryDelete(DeleteView): 
	model = Category

class ProductDelete(DeleteView): 
	model = Product
