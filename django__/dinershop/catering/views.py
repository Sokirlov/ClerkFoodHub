import datetime
from django.shortcuts import render
from .models import Provider, CategoryFood, Food, Orders
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

class FoodAllView(ListView):
    model = CategoryFood
    template_name = 'catering/main.html'
    context_object_name = 'foods'
    queryset = CategoryFood.objects.all().prefetch_related('food_set')

    def post(self, request, *args, **kwargs):
        form = request.POST


        for i in form:
            if i  != 'csrfmiddlewaretoken':
                order = i.split(' - ')
                print(order)
                order_date = datetime.datetime.strptime(order[1], '%d %B %Y г. %H:%M')
                print(order_date, type(order_date))
        return self.get(request, *args, **kwargs)

