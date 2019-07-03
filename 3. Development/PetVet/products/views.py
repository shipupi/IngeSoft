from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Product, Category
from cart.forms import CartAddProductForm
from django.core.paginator import Paginator
from django.db.models import Q


# Create your views here.

def product_list(request, slug=None):
    category = None
    price_min = request.GET.get("price_min", 0)
    price_max = request.GET.get("price_max", 1000000)
    search= request.GET.get("search", None)
    per_page = 12
    page = request.GET.get("page")
    categories = Category.objects.all()
    if slug:
        category = get_object_or_404(Category, slug=slug)
        products = category.products.all()
    else:
        products = Product.objects.all()

    products = products.filter(available=True, price__lte=price_max,
                price__gte=price_min)

    if search:
        products = products.filter(available=True, price__lte=price_max,
            price__gte=price_min, name__icontains=search)

    print(len(products))
    paginator = Paginator(products, per_page)
    products = paginator.get_page(page)
    context = {
        'category' : category,
        'categories' : categories,
        'products' : products,
    }
    context['category'] = category
    return render(request, 'products/product_list.html', context)

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    context = {
            'product' : product,
            'cart_product_form': cart_product_form

    }
    return render(request, 'products/product_detail.html', context)