from django.shortcuts import render, redirect
from django.urls import reverse
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart

# Create your views here.

def orders_list(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)
        return render(request, 'orders/list.html', {'orders': orders})
    else:
        return redirect(reverse('login_page)'))

def order_create(request):
    cart = Cart(request)
    form = OrderCreateForm(request.POST)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(reverse('login_page)'))
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
            return redirect(reverse('orders:orders_list'))
        else:
            print('invalid form')
            return render(request, "cart/detail.html", {'form': form, 'cart': cart})
    return redirect(reverse('cart:cart_detail'))
