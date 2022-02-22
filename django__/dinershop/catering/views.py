import datetime
from django.shortcuts import render
from django.contrib.auth.models import User
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
        user_raw = request.user.username
        user = User.objects.get(username=user_raw)
        print(user)
        for i in form:
            if i  != 'csrfmiddlewaretoken':
                order = i.split(' - ')
                order_date = datetime.datetime.strptime(order[1], '%d/%m/%Y %H:%M')
                food = Food.objects.get(title=order[0])
                Orders.objects.create(user=user, food=food, quantity=1, order_for_day=order_date)

                # print(order[0], order_date, type(order_date))
        return self.get(request, *args, **kwargs)

