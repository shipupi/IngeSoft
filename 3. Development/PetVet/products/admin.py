from django.contrib import admin
from django.contrib import admin 
from .models import Products
from .models import Category
# Register your models here.

admin.site.register(Category)
admin.site.register(Products)
