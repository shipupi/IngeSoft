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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from products import views as products_views
from .views import *

urlpatterns = [
	path('', index, name='index'),
	# path('', login_page, name='login_page'),
	path('registration/', register_page, name='register_page'),
	path('registration-complete/', register_complete_page, name='register_complete_page'),
	path('admin/', admin.site.urls, name='admin'),

	# Includes
    path('cart', include('cart.urls')),
    path('', include('products.urls')), # ESTE TIENE Q IR ULTIMO!!
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
