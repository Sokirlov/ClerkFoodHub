from django.urls import include, path
from django.contrib.auth.decorators import login_required
from .views import FoodAllView


urlpatterns = [
    path('', login_required(FoodAllView.as_view()), name='main'),
    # path()
]