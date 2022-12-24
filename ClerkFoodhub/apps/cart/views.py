import datetime
from typing import Dict, Any
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from rest_framework import generics
from rest_framework import permissions
from django.contrib.auth.models import User

from django.db.models import Prefetch
from django.views.generic import ListView, DetailView
from rest_framework import viewsets
from catering.models import Provider, CategoryFood, Food
from cart.models import Orders
from cart.serializers import ProvidersSerializer, FoodSerializer, CategoryFoodSerializer, OrdersUserSerializer


class FoodViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Food.objects.filter(is_active=1)
    serializer_class = FoodSerializer
#
class CategoryFoodViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CategoryFood.objects.all().prefetch_related(
            Prefetch('foods', queryset=Food.objects.filter(is_active=1)))
    serializer_class = CategoryFoodSerializer

class ProvidersViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    raw_queryset = Provider.objects.all().prefetch_related(
        Prefetch('categorysfoods', queryset=CategoryFood.objects.all().prefetch_related(
            Prefetch('foods', queryset=Food.objects.filter(is_active=1))
        )))

    queryset = raw_queryset
    serializer_class = ProvidersSerializer
    # permission_classes = [permissions.IsAuthenticated]



class OrdersUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Orders.objects.all()
    serializer_class = OrdersUserSerializer
    def get_queryset(self):
        return Orders.objects.filter(user__departament=self.request.user.departament.id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# class DepartamentOrdersViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = Orders.objects.all()
#     serializer_class = DepartamentOrdersSerializer
#     def get_queryset(self):
#         # print(f'DEPARTAMENT = {self.request.user.departament.date_add}')
#         return Orders.objects.filter(user__departament=self.request.user.departament.id)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)



# def make_food_set(form):
#     order = {}
#     for i in form:
#         if i != 'csrfmiddlewaretoken':
#             # print(f'i - {i}')
#             order_dish_date = i.split(' - ')
#             order_date = order_dish_date[2]
#             order_dish = Food.objects.get(id=order_dish_date[0])
#             try:
#                 order_key = order[order_date]
#                 order_key.append(order_dish)
#                 order[order_date] = order_key
#             except:
#                 order[order_date] = [order_dish,]
#     return order


class FoodAllView(ListView):
    model = Provider
    template_name = 'catering/manu.html'
    context_object_name = 'providers'
    # raw_queryset = Provider.objects.all().prefetch_related()  # Prefetch('provider_set', queryset=Food.objects.filter(is_active=1)))
    raw_queryset = Provider.objects.all().prefetch_related(
        Prefetch('categorysfoods', queryset=CategoryFood.objects.all().prefetch_related(
            Prefetch('foods', queryset=Food.objects.filter(is_active=1))
        )))
    queryset = raw_queryset
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



# class ReadyToOrdered(ListView):
#     def sorting_by_day(orders):
#         new_list: dict[str, Any] = dict()
#         for ord in orders:
#             try:
#                 foodlist = new_list[str(ord.order_for_day)]
#                 for i in ord.food.all():
#                     if i in foodlist:
#                         foodlist[i]['quantity'] += 1
#                     else:
#                         foodlist[i] = i.__dict__
#                         foodlist[i]['quantity'] = 1
#             except:
#                 foodlist = dict()
#                 for i in ord.food.all():
#                     foodlist[i] = i.__dict__
#                     foodlist[i]['quantity'] = 1
#                 new_list[str(ord.order_for_day)] = foodlist
#         return new_list
#     model = Orders
#     future_orders = Orders.objects.filter(order_for_day__gte=datetime.datetime.today())
#     queryset = sorting_by_day(future_orders)
#     template_name = 'catering/order_cart.html'
#     context_object_name = 'dishes'

class DashBoardOrders(ListView):

    def sorting_by_day():
        # new_list: dict[int, Any] = dict()
        new_list = list()
        for d in range(1, 7, 1):
            the_day = (datetime.datetime.today() + datetime.timedelta(days=d))
            if the_day.isoweekday() in range(1, 5):
                # print('id -', d, '-', the_day.isoweekday())
                rq = Orders.objects.filter(order_for_day=the_day)
                new_list.append(rq)
                # print('new_list -', new_list[f'{d}'])
        # print(new_list)
        return new_list
    model = Orders
    # future_orders = Orders.objects.filter(order_for_day__gte=datetime.datetime.today() + datetime.timedelta(days=1))#, user=request.user.username)
    # future_orders = Orders.objects.filter(order_for_day__gte=datetime.datetime.today() + datetime.timedelta(days=10))
    queryset = sorting_by_day()
    context_object_name = 'dashboard'
    template_name = 'cart/orders_list.html'