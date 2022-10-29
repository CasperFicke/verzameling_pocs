# stocks/urls.py

# Django
from django.urls import path

# local
from . import views
# import views

urlpatterns = [
  path('stocks/'                  , views.all_stocks, name="all_stocks"),
  path('stocks/<stock_id>/edit/'  , views.edit_stock, name="edit_stock"),
  path('stocks/<stock_id>/delete/', views.delete_stock, name="delete_stock"),
  path('stocks/values/'           , views.stockvalues, name="stockvalues"),
]
