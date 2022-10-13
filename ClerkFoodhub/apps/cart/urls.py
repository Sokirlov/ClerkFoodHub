from django.urls import include, path
from django.contrib.auth.decorators import login_required
from .views import FoodAllView #, ReadyToOrdered


urlpatterns = [
    path('', login_required(FoodAllView.as_view()), name='main'),
    # path('cart/', login_required(ReadyToOrdered.as_view()), name='cart')
]