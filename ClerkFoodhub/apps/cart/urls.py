from django.urls import include, path
from django.contrib.auth.decorators import login_required
from rest_framework import routers
from . import views
# from .views import FoodAllView, OrdersViewSet, OrdersViewSet

router = routers.DefaultRouter()
# router.register(r'providers', views.ProviderViewSet)
router.register(r'add-order', views.OrdersViewSet)
# router.register(r'add-order', views.OrdersViewSet.as_view())
router.register(r'Menu-all-foods', views.ProvidersViewSet)


app_name = 'cart'

urlpatterns = [
    path('', login_required(views.FoodAllView.as_view()), name='main'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    # path('cart/', login_required(ReadyToOrdered.as_view()), name='cart')
]