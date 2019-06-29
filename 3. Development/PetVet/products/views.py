from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Product, Category

# Create your views here.

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
