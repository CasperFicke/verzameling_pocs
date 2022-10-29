# store/admin.py

# django
from django.contrib import admin

# Local
from .models import Customer, Product, Category, Tag, Order, OrderItem, ShippingAddress

# Register Product
class ProductAdmin(admin.ModelAdmin):
  list_display        = ('name', 'price', 'aantal', 'digital')
  list_filter         = ('name','digital')
  ordering            = ('name',)

# Register Order
class OrderAdmin(admin.ModelAdmin):
  list_display        = ('transaction_id', 'date_ordered', 'customer', 'complete')
  list_filter         = ('transaction_id','customer')
  ordering            = ('transaction_id',)

# Register OrderItem
class OrderItemAdmin(admin.ModelAdmin):
  list_display        = ('order', 'quantity', 'product')
  list_filter         = ('order','product')
  ordering            = ('order',)
  
# overall admin area 
admin.site.register(Customer)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShippingAddress)