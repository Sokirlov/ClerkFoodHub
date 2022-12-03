from django.contrib.auth.models import User, Group
from rest_framework import serializers
from catering.models import Food, CategoryFood, Provider
from users.models import CustomUser
from .models import Orders




class UserSerializer(serializers.HyperlinkedModelSerializer):
    departament = serializers.StringRelatedField(many=False, read_only=True)
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "departament"]



class FoodSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Food
        fields = ["title", "description", "price", "buy_link", "image", "link", "id_sort", "is_active", "date_add", "last_update"]

class CategoryFoodSerializer(serializers.HyperlinkedModelSerializer):
    foods = FoodSerializer(many=True, read_only=True)
    class Meta:
        model = CategoryFood
        fields = ["title", "link", "id_sort", "date_add", "foods"]


class ProvidersSerializer(serializers.HyperlinkedModelSerializer):
    district = serializers.StringRelatedField(many=False, read_only=True)
    categorysfoods = CategoryFoodSerializer(many=True, read_only=True)

    class Meta:
        model = Provider
        fields = ("title", "link", "id_sort", "date_add", "min_order", "district", "categorysfoods")
        read_only_fields = ("title", "link", "id_sort", "date_add", "min_order", "district", "categorysfoods")


class OrdersUserSerializer(serializers.ModelSerializer):
    catering = serializers.PrimaryKeyRelatedField(many=False, queryset=Provider.objects.all())
    food = serializers.PrimaryKeyRelatedField(many=False, queryset=Food.objects.filter(is_active=1))
    user = UserSerializer(read_only=True)
    class Meta:
        model = Orders
        fields = ["id", "user", "data_add", "catering", "food", "quantity", "order_for_day", "provider_cart_id"]
        read_only_fields = ("id", "user",)