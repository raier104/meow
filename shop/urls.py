from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path("products/", views.product_list, name="product_list"),
    path("cart/", views.cart, name="cart"),  # Add URL pattern for 'cart'
    path("contact/", views.contact, name="contact"),  # Add URL pattern for 'contact'
    path("shop/", views.shop, name="shop"),  # Add URL pattern for 'shop' page
    path("food/", views.food, name="food"),  # Add URL pattern for 'food' page
    path("cloth/", views.cloth, name="cloth"),  # Add URL pattern for 'cloth' page
    path("toy/", views.toy, name="toy"),  # Add URL pattern for 'toy' page
    path("carrier/", views.carrier, name="carrier"),  # Add URL pattern for 'carrier' page
    path("medicine/", views.medicine, name="medicine"),  # Add URL pattern for 'medicine' page
    path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),  # Add URL pattern for 'add_to_cart' functionality
    path("add-product/", views.add_product, name="add_product"),
    path("update-product/<int:product_id>/", views.update_product, name="update_product"),
    path("delete-product/<int:product_id>/", views.delete_product, name="delete_product"),
    path("payment/", views.payment, name="payment"),
    path("payment/details/", views.payment_details, name="payment_details"),
    path("payment/success/", views.payment_success, name="payment_success"),
    path("previous-orders/", views.previous_orders, name="previous_orders"),
    path("receipt/<int:receipt_id>/download/", views.download_receipt, name="download_receipt"),
    path("search/", views.search_products, name="search"),
]
