from django.shortcuts import render, redirect
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart

# Create your views here.

def orders_list(request):
    if request.user.is_authenticated:
        orders = Order.objects.all()
        return render(request, 'orders/list.html', {'orders': orders})
    else:
        return redirect('/login')



def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('/login')
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            order.user.add(*[request.user])
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
        return redirect('/cart')
