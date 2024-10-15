from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from carts.models import Cart, CartItem
from products.models import Product
from carts.serializers import CartSerializer, CartItemSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated


# Ensure that all views require authentication
# @permission_classes([IsAuthenticated])
@api_view(["GET"])
def get_cart(request):
    """
    Retrieve the cart for the authenticated user.
    """
    cart, created = Cart.objects.get_or_create(user=request.user)
    serializer = CartSerializer(cart)
    return Response(serializer.data)


# @permission_classes([IsAuthenticated])
@api_view(["POST"])
def add_to_cart(request):
    """
    Add a product to the cart for the authenticated user.
    """
    product_id = request.data.get("product_id")
    quantity = request.data.get("quantity", 1)

    # Get the product or return a 404 error if not found
    product = get_object_or_404(Product, id=product_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if the item already exists in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:  # If the item already exists, update the quantity
        cart_item.quantity += quantity
        cart_item.save()

    return Response(
        {"success": "Product added to cart"}, status=status.HTTP_201_CREATED
    )


# @permission_classes([IsAuthenticated])
@api_view(["PUT", "DELETE"])
def update_cart_item(request, item_id):
    """
    Update or delete a cart item.
    """
    cart_item = get_object_or_404(CartItem, id=item_id)

    if request.method == "PUT":
        quantity = request.data.get("quantity")
        if quantity is not None and quantity > 0:  # Check for valid quantity
            cart_item.quantity = quantity
            cart_item.save()
            return Response({"success": "Cart item updated"}, status=status.HTTP_200_OK)

    elif request.method == "DELETE":
        cart_item.delete()
        return Response(
            {"success": "Cart item deleted"}, status=status.HTTP_204_NO_CONTENT
        )

    return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
