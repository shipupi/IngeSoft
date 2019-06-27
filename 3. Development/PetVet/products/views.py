from django.shortcuts import render
from django.views.generic import ListView, DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Products
from .models import Category

# Create your views here.

class CategoryList(ListView): 
	model = Category

class ProductsList(ListView): 
	model = Products

class CategoryDetail(DetailView): 
	model = Category

class ProductsDetail(DetailView): 
	model = Products

class CategoryCreate(CreateView): 
	model = Category

class ProductsCreate(CreateView): 
	model = Products

class CategoryUpdate(UpdateView): 
	model = Category

class ProducsUpdate(UpdateView): 
	model = Products

class CategoryDelete(DeleteView): 
	model = Category

class ProductsDelete(DeleteView): 
	model = Products