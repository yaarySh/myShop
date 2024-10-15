from rest_framework import serializers
from .models import Cart, CartItem
from products.serializers import (
    ProductSerializer,
)  # Make sure to import the Product serializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()  # Nesting the Product serializer

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity"]  # Include necessary fields


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)  # Nested items

    class Meta:
        model = Cart
        fields = ["id", "user", "items"]  # Include necessary fields
        read_only_fields = [
            "user"
        ]  # User should not be modifiable through this serializer
