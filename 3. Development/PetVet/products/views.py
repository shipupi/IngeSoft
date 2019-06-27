from django.shortcuts import render
from django.views.generic import ListView, DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Product
from .models import Category

# Create your views here.

class CategoryList(ListView): 
	model = Category

class ProductsList(ListView): 
	model = Product

class CategoryDetail(DetailView): 
	model = Category

class ProductsDetail(DetailView): 
	model = Product

class CategoryCreate(CreateView): 
	model = Category

class ProductsCreate(CreateView): 
	model = Product

class CategoryUpdate(UpdateView): 
	model = Category

class ProducsUpdate(UpdateView): 
	model = Product

class CategoryDelete(DeleteView): 
	model = Category

class ProductsDelete(DeleteView): 
	model = Product