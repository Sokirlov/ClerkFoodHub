import datetime
import locale, sys
from typing import Dict, Any
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from rest_framework import generics
from rest_framework import permissions
from django.contrib.auth.models import User

from django.http import Http404
from django.utils.translation import gettext as _
from .forms import OrdersForm
from django.shortcuts import redirect
from django.db.models import Prefetch
from django.views.generic import ListView, DetailView
from rest_framework import viewsets
from catering.models import Provider, CategoryFood, Food
from users.models import CustomUser
from cart.models import Orders
from cart.serializers import ProvidersSerializer, FoodSerializer, CategoryFoodSerializer, OrdersUserSerializer


class FoodViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Food.objects.filter(is_active=1)
    serializer_class = FoodSerializer

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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_day'] = self.request.GET.get('order_day')
        return context

    def post(self, request, *args, **kwargs):
        form = request.POST
        order_for_day = datetime.datetime.strptime(form['order_day'], '%d-%m-%Y')
        user_raw = request.user.username
        user = CustomUser.objects.get(username=user_raw)
        for name, orders in form.items():
            if name == 'csrfmiddlewaretoken' or name == 'order_day':
                continue
            else:
                dish = Food.objects.get(id=name)
                # "data_add", "user", "catering", "food", "quantity", "order_for_day", "payer", "provider_cart_id",
                Orders.objects.create(
                    data_add=datetime.datetime.now(),
                    user=user,
                    catering=dish.category.provider,
                    food=dish,
                    quantity=orders[0],
                    order_for_day=order_for_day)
        print(user, order_for_day, )
        # return self.get(request, *args, **kwargs)
        return redirect('/')



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
        if sys.platform == 'win32':
            locale.setlocale(locale.LC_ALL, 'ukr_ukr')
        else:
            locale.setlocale(locale.LC_ALL, 'uk_UA.UTF-8')
        new_list: dict[int, Any] = dict()
        for d in range(1, 8, 1):
            the_day = (datetime.datetime.today() + datetime.timedelta(days=d))
            if the_day.isoweekday() in range(1, 6):
                new_list[datetime.datetime.strftime(the_day, '%A')] ={
                    "orders": Orders.objects.filter(order_for_day=the_day),
                    "order_date": the_day,
                }

        return new_list
    model = Orders
    # future_orders = Orders.objects.filter(order_for_day__gte=datetime.datetime.today() + datetime.timedelta(days=1))#, user=request.user.username)
    # future_orders = Orders.objects.filter(order_for_day__gte=datetime.datetime.today() + datetime.timedelta(days=10))
    queryset = sorting_by_day()
    context_object_name = 'dashboard'
    template_name = 'cart/orders_list.html'

