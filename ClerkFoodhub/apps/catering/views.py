import datetime
from typing import Dict, Any

from django.shortcuts import render
from django.db.models import Prefetch
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from catering.models import Provider, CategoryFood, Food, Orders
# from clients.models import Worker

def make_food_set(form):
    order = {}
    for i in form:
        if i != 'csrfmiddlewaretoken':
            # print(f'i - {i}')
            order_dish_date = i.split(' - ')
            order_date = order_dish_date[2]
            order_dish = Food.objects.get(id=order_dish_date[0])
            try:
                order_key = order[order_date]
                order_key.append(order_dish)
                order[order_date] = order_key
            except:
                order[order_date] = [order_dish,]
    return order


# class FoodAllView(ListView):
#     model = CategoryFood
#     template_name = 'catering/main.html'
#     context_object_name = 'foods'
#     raw_queryset = CategoryFood.objects.all().prefetch_related(Prefetch('food_set', queryset=Food.objects.filter(is_active=1)))
#     queryset = raw_queryset
#
#     def post(self, request, *args, **kwargs):
#         form = request.POST
#         user_raw = request.user.username
#         user = Worker.objects.get(username=user_raw)
#         order_list = make_food_set(form)
#         for key, order in order_list.items():
#             order_date = datetime.datetime.strptime(key, '%d/%m/%Y %H:%M')
#             new_order = Orders.objects.create(user=user, quantity=1, order_for_day=order_date)
#             for dish in order:
#                 new_order.food.add(dish)
#         return self.get(request, *args, **kwargs)



class ReadyToOrdered(ListView):
    def sorting_by_day(orders):
        new_list: dict[str, Any] = dict()
        for ord in orders:
            try:
                foodlist = new_list[str(ord.order_for_day)]
                for i in ord.food.all():
                    if i in foodlist:
                        foodlist[i]['quantity'] += 1
                    else:
                        foodlist[i] = i.__dict__
                        foodlist[i]['quantity'] = 1
            except:
                foodlist = dict()
                for i in ord.food.all():
                    foodlist[i] = i.__dict__
                    foodlist[i]['quantity'] = 1
                new_list[str(ord.order_for_day)] = foodlist
        return new_list
    model = Orders
    future_orders = Orders.objects.filter(order_for_day__gte=datetime.datetime.today())
    queryset = sorting_by_day(future_orders)
    template_name = 'catering/order_cart.html'
    context_object_name = 'dishes'