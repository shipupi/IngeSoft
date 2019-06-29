from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Product, Category

# Create your views here.

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)

    context = {
            'category' : category,
            'categories' : categories,
            'products' : products
    }
    print(products)
    print(products[0].name)
    return render(request, 'products/product_list.html', context)

def products_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    context = {
            'product' : product
    }
    return render(request, 'products/detail.html', context)

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
