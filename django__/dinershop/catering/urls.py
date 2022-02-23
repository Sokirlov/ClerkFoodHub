from django.urls import include, path
from .views import FoodAllView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', login_required(FoodAllView.as_view()), name='main')
]