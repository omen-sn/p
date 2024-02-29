from rest_framework import serializers
from .models import Category, Product, TagProduct, ProductDetail


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        # Використовуйте `self.context['request'].user` для доступу до користувача з контексту запиту
        user = self.context['request'].user
        return Product.objects.create(user=user, **validated_data)

class TagProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagProduct
        fields = '__all__'

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetail
        fields = '__all__'