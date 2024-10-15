from django.urls import path
from carts import views

urlpatterns = [
    path(
        "", views.get_cart, name="get_cart"
    ),  # To retrieve the cart for the authenticated user
    path("add/", views.add_to_cart, name="add_to_cart"),  # To add a product to the cart
    path(
        "<int:item_id>/", views.update_cart_item, name="update_cart_item"
    ),  # To update or delete a specific cart item
]
