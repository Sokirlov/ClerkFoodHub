from django.shortcuts import render
from .models import Provider, CategoryFood, Food, Orders
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

class FoodAllView(ListView):
    model = CategoryFood
    template_name = 'catering/main.html'
    context_object_name = 'foods'
    queryset = CategoryFood.objects.all().prefetch_related('food_set')
