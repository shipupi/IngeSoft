from django.shortcuts import render, redirect
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from django import forms

# Create your views here.

def orders_list(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)
        return render(request, 'orders/list.html', {'orders': orders})
    else:
        return redirect('/login')

def order_create(request):
    cart = Cart(request)
    form = OrderCreateForm(request.POST)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('/login')
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            return redirect('/orders')
        else:
            return render(request, "cart/detail.html", {'form': form, 'cart': cart})
    return redirect('/cart')
