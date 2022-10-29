# store/urls.py

# Django
from django.urls import path

# local
from . import views

urlpatterns = [
  # Store
  path('store/'          , views.index, name="index-store"),
  path('store/staff/'    , views.staff, name="staff"),
  path('store/profile/'  , views.profile, name="profile"),
  # products
  path('store/products/'              , views.products, name="products"),
  path('store/products/<product_id>/' , views.show_product, name="show-product"),
  # webshop
  path('store/orders/'        , views.orders, name="orders"),
  path('store/store/'         , views.store, name="store"),
  path('store/cart/'          , views.cart, name="cart"),
  path('store/checkout/'      , views.checkout, name="checkout"),
  path('store/update_item/'   , views.updateItem, name="update-item"),
  path('store/process_order/' , views.processOrder, name="process-order"),
]

