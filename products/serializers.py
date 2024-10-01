from rest_framework import serializers
from products.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(
        many=True, read_only=True
    )  # Adjust according to your actual category serializer

    class Meta:
        model = Product
        fields = "__all__"
