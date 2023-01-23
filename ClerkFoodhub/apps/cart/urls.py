from django.urls import include, path
from django.contrib.auth.decorators import login_required
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
# router.register(r'providers', views.ProviderViewSet)
router.register(r'all_add-order_by_department', views.OrdersUserViewSet)
router.register(r'all-foods', views.ProvidersViewSet)
# router.register(r'departament', views.DepartamentOrdersViewSet)


app_name = 'cart'

urlpatterns = [
    path('', login_required(views.DashBoardOrders.as_view()), name='main'),
    path('ct/', login_required(views.FoodAllView.as_view()),  name='cart'),
    path('spliwise/', login_required(views.Splitwise), name='spliwise'),
    path('hystory/', login_required(views.MyOrderHystory), name='history'),
    path('buy/', login_required(views.BuyOrderInCatering), name='buycart'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    # path('cart/', login_required(ReadyToOrdered.as_view()), name='cart')
]