import datetime, locale, sys, copy
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
from cart.serializers import ProvidersSerializer, FoodSerializer, CategoryFoodSerializer, OrdersUserSerializer
from catering.models import Provider, CategoryFood, Food
from users.models import Departament, CustomUser
from cart.models import Orders


# -------------------------- API views-----------------
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


# ------------------------- local views ---------------

class FoodAllView(ListView):
    model = Provider
    template_name = 'catering/manu.html'
    context_object_name = 'providers'
    queryset = Provider.objects.all().prefetch_related(
        Prefetch('categorysfoods', queryset=CategoryFood.objects.all().prefetch_related(
            Prefetch('foods', queryset=Food.objects.filter(is_active=1))
        ))
    )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        order_day = self.request.GET.get('order_day')
        if not order_day:
            order_day = (datetime.datetime.now()+ datetime.timedelta(days=1)).strftime('%d-%m-%Y')
        context['order_day'] = order_day
        order_for_day = datetime.datetime.strptime(order_day, '%d-%m-%Y')
        context['ordered'] = Orders.objects.filter(order_for_day=order_for_day, user=self.request.user.id)
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
                try:
                    allredy_ordered = Orders.objects.get(user=user, food=dish, order_for_day=order_for_day)
                except:
                    allredy_ordered = None
                if allredy_ordered:
                    if int(orders[0]) == 0:
                        allredy_ordered.delete()
                    elif allredy_ordered.quantity != int(orders[0]):
                        allredy_ordered.quantity = orders[0]
                        allredy_ordered.save()

                else:
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

class DashBoardOrders(ListView):
    model = Orders
    queryset = Orders.objects.all()#.filter(order_for_day__gte=datetime.datetime.today() + datetime.timedelta(days=1))
    # future_orders = Orders.objects.filter(order_for_day__gte=datetime.datetime.today() + datetime.timedelta(days=10))
    # queryset = sorting_by_day()
    context_object_name = 'dashboard_all'
    template_name = 'cart/orders_list.html'

    def sorting_by_day(self):
        if sys.platform == 'win32':
            locale.setlocale(locale.LC_ALL, 'ukr_ukr')
        else:
            locale.setlocale(locale.LC_ALL, 'uk_UA.UTF-8')
        new_list: dict[int, Any] = dict()
        for d in range(1, 8, 1):
            the_day = (datetime.datetime.today() + datetime.timedelta(days=d))
            if the_day.isoweekday() in range(1, 6):
                new_list[datetime.datetime.strftime(the_day, '%A')] ={
                    "orders": Orders.objects.filter(order_for_day=the_day, user=self.request.user),
                    "order_date": the_day,
                }
        return new_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dashboard'] = self.sorting_by_day()
        return context

def _get_uaser_set(all_order):
    userset = {}
    for i in all_order:
        if i.user.departament not in userset:
            userset[i.user.departament] = [i.user,]
        elif i.user not in userset[i.user.departament]:
            userset[i.user.departament].append(i.user)
    print(userset)
    return userset

def _colapse_order_by_user(all_orders):
    clients = _get_uaser_set(all_orders)
    orders = {}
    for dep, client_list in clients.items():
        orders[dep] = {}
        for client in client_list:
            client_order_sum = 0
            client_order_id = []
            client_order = all_orders.filter(user=client)
            order_provider = {}
            for i in client_order:
                this_provider = i.food.category.provider
                if this_provider not in order_provider:
                    client_order_id.append(i.id)
                    client_order_sum += (i.food.price * i.quantity)
                    order_provider[this_provider] = dict(user=client, order_sum=client_order_sum, order_id=client_order_id)
                else:
                    order_provider[this_provider]['order_id'].append(i.id)
                    order_provider[this_provider]['order_sum'] += (i.food.price * i.quantity)
            orders[dep][client] = order_provider
    return orders

# def _get_my_catering

def BuyOrderInCatering(request):
    """
    :request: страница заказа в кейтеренге
    :return: Вывод всех пользователе компании сгрупированных по отделам, (пользователей, сумма заказа, ID заказов).

    """
    order_day = request.GET.get('order_day')
    if not order_day:
        order_day = (datetime.datetime.now() + datetime.timedelta(days=1))
    all_ordered_on_day = Orders.objects.filter(order_for_day=order_day, user__departament__company=request.user.departament.company, payer=None)
    all_department = Departament.objects.filter(company=request.user.departament.company)
    my_order = _colapse_order_by_user(all_ordered_on_day.filter(user=request.user, payer=None))
    orders_by_user = _colapse_order_by_user(all_ordered_on_day.exclude(user=request.user))
    # my_cattering = Provider.objects.get()

    if request.POST:
        form_orders = copy.copy(request.POST)
        form_orders.pop('csrfmiddlewaretoken')
        for i in form_orders:
            orders_ids = i.replace('[', '').replace(']', '').split(',')
            for j in orders_ids:
                order = Orders.objects.get(id=j)
                order.payer = request.user
                order.save()
        print('ppp', form_orders)
        return redirect('/')
    return render(request, 'cart/catering_cart.html', {
        'payed_orders': all_ordered_on_day,
        'my_order': my_order,
        'orders_by_user': orders_by_user
    })

def Splitwise(request):
    client = request.user
    payed_orders = Orders.objects.filter(payer=client)

    return render(request, 'cart/splitwise.html', {'payed_orders': payed_orders, })

