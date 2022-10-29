# store/models.py

from django.db import models
from django.contrib.auth.models import User

# Customer
class Customer(models.Model):
  name  = models.CharField(max_length=200, null=True)
  email = models.EmailField(max_length=200)
  # relaties
  user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)

  # method om model in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return f'{self.name} user {self.user.last_name}'

# Category model
class Category(models.Model):
  name        = models.CharField(max_length=50, unique=True)
  description = models.TextField(max_length=200, null=True, blank=True)

  class Meta:
    verbose_name_plural = 'categories'

  # functie om object in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return self.name

# Tag model
class Tag(models.Model):
  name        = models.CharField(max_length=50, unique=True)
  description = models.TextField(max_length=200, null=True, blank=True)

  class Meta:
    verbose_name_plural = 'tags'

  # functie om object in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return self.name

# Product
class Product(models.Model):
  name     = models.CharField(max_length=200)
  price    = models.DecimalField(max_digits=7, decimal_places=2)
  digital  = models.BooleanField(default=False, null=True, blank=True)
  image    = models.ImageField(null=True, blank=True)
  aantal   = models.PositiveIntegerField(null=True, blank=True)
  # relaties
  category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
  tags     = models.ManyToManyField(Tag, blank=True, related_name='products')

  class Meta:
    verbose_name_plural = 'Producten'

  def __str__(self):
    return self.name
  # return empty url if product has no image
  @property
  def imageURL(self):
    try:
      url = self.image.url
    except:
      url = ''
    return url

# Order
class Order(models.Model):
	transaction_id = models.CharField(max_length=100, null=True)
	complete       = models.BooleanField(default=False)
	date_ordered   = models.DateTimeField(auto_now_add=True)
  # relaties
	customer       = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)

  # method om model in de admin web-pagina te kunnen presenteren
	def __str__(self):
		return str(self.transaction_id)

	# determine if shipping is needed
	@property
	def shipping(self):
		shipping   = False
		orderitems = self.orderitems.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping
  # calculate total price of order
	@property
	def get_cart_total(self):
		orderitems = self.orderitems.all()
		total      = sum([item.get_total for item in orderitems])
		return total
  # calculate total number of intems in the order
	@property
	def get_cart_items(self):
		orderitems = self.orderitems.all()
		total      = sum([item.quantity for item in orderitems])
		return total 

# Orderitem
class OrderItem(models.Model):
  quantity   = models.IntegerField(default=0, null=True, blank=True)
  date_added = models.DateTimeField(auto_now_add=True)
  # relaties
  order      = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, related_name='orderitems')
  product    = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

  # method om model in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return str(self.product)

  # calculate totalprice for ordered product
  @property
  def get_total(self):
    total = self.product.price * self.quantity
    return total

# Shipping adres
class ShippingAddress(models.Model):
  address    = models.CharField(max_length=200, null=False)
  city       = models.CharField(max_length=200, null=False)
  state      = models.CharField(max_length=200, null=False)
  zipcode    = models.CharField(max_length=200, null=False)
  country    = models.CharField(max_length=100, default="Nederland", null=False)
  date_added = models.DateTimeField(auto_now_add=True)
	# relaties
  customer   = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name='shippingadresses')
  order      = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)

  class Meta:
    verbose_name_plural = 'Shipping adresses'

  # method om model in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return self.address