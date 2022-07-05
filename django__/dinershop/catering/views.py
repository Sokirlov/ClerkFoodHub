import datetime
from django.shortcuts import render
from django.db.models import Prefetch
from django.contrib.auth.models import User
from .models import Provider, CategoryFood, Food, Orders
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

def make_food_set(form):
    order = {}
    for i in form:
        if i != 'csrfmiddlewaretoken':
            order_dish_date = i.split(' - ')
            order_date = order_dish_date[1]
            order_dish = Food.objects.get(title=order_dish_date[0])
            try:
                order_key = order[order_date]
                order_key.append(order_dish)
                order[order_date] = order_key
            except:
                order[order_date] = [order_dish,]
    return order


class FoodAllView(ListView):
    model = CategoryFood
    template_name = 'catering/main.html'
    context_object_name = 'foods'
    raw_queryset = CategoryFood.objects.all().prefetch_related(Prefetch('food_set', queryset=Food.objects.filter(is_active=1)))
    queryset = raw_queryset

    def post(self, request, *args, **kwargs):
        form = request.POST
        user_raw = request.user.username
        user = User.objects.get(username=user_raw)
        order_list = make_food_set(form)
        print(user, order_list)
        for key, order in order_list.items():
                order_date = datetime.datetime.strptime(key, '%d/%m/%Y %H:%M')
                new_order = Orders.objects.create(user=user, quantity=1, order_for_day=order_date)
                for dish in order:
                    new_order.food.add(dish)
        return self.get(request, *args, **kwargs)

class ReadyToOrdered(ListView):
    model = Orders
    queryset = Orders.objects.filter(order_for_day__gte=datetime.datetime.today())