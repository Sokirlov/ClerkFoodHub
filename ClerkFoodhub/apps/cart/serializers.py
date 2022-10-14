from django.contrib.auth.models import User, Group
from rest_framework import serializers

from catering.models import Food, CategoryFood, Provider
from users.models import CustomUser
from django.contrib.auth import get_user_model

from .models import Orders

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name"]



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
    district = serializers.StringRelatedField(many=False)
    # provider = serializers.StringRelatedField(many=False)
    # categoryfood = serializers.StringRelatedField(many=True)
    categorysfoods = CategoryFoodSerializer(many=True, read_only=True)
    # categoryfood = serializers.SlugRelatedField(
    #         many=True,
    #         read_only=True,
    #         slug_field='title',
    #         # view_name='category-detail'
    #     )

    class Meta:
        model = Provider
        # fields = '__all__'
        fields = ["title", "link", "id_sort", "date_add", "min_order", "district", "categorysfoods"]



# class OrdersSerializer(generics.ListCreateAPIView):
class OrdersSerializer(serializers.ModelSerializer):
    # client = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    # client = serializers.SerializerMethodField('get_user')
    # user = serializers.PrimaryKeyRelatedField(many=False, queryset=CustomUser.objects.all())
    catering = serializers.PrimaryKeyRelatedField(many=False, queryset=Provider.objects.all())
    food = serializers.PrimaryKeyRelatedField(many=False, queryset=Food.objects.filter(is_active=1))
    # payer = serializers.PrimaryKeyRelatedField(many=False, queryset=CustomUser.objects.all())
    # payer = serializers.PrimaryKeyRelatedField(many=True)
    # food = serializers.PrimaryKeyRelatedField(many=True)
    # provider = ProvidersSerializer(many=True)
    # client = serializers.PrimaryKeyRelatedField(many=True)
    class Meta:
        model = Orders
        fields = ["data_add", "catering", "food", "quantity", "order_for_day", "provider_cart_id"]


    # def save(self):
    #     self.client = self.context['request'].user
    #     return self

    # def get_user(self):
    #     request = self.context
    #     return request.user


# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']