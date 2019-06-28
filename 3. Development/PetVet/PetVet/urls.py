"""PetVet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import login_page, register_page
from products import views as products_views
from .views import login_page, register_page, cart_page

urlpatterns = [
	path('', login_page, name='login_page'),
	path('registration/', register_page, name='register_page'),
	path('admin/', admin.site.urls, name='admin'),
    path('cart/', cart_page, name='cart_page'),

	# products
	path('products', products_views.ProductsList.as_view(), name='product_list')
]
