from django.urls import include, path
from .views import FoodAllView


urlpatterns = [
    path('', FoodAllView.as_view(), name='main')
]