# store/views.py

# django
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, JsonResponse
import json
import datetime

# local
from .models import User, Product, Order, OrderItem, ShippingAddress
from .utils import cartData, guestOrder

# index
@login_required
def index(request):
  title    = 'index'
  products = Product.objects.all()
  context = {
    'title'    : title,
    'products' : products
  }
  return render(request, 'store/index.html', context)

# staff
@login_required
def staff(request):
  title = 'staff'
  staff = User.objects.all()
  staffCount = staff.count()
  context = {
    'title': title,
    'staff': staff,
    'staffCount': staffCount
  }
  return render(request, 'store/staff.html', context)
  
# profile
def profile(request):
  title = 'profile'
  context = {
    'title': title
  }
  return render(request, 'store/profile.html', context)
  
# products
@login_required
def products(request):
  title    = 'products'
  products = Product.objects.all()
  context = {
    'title'    : title,
    'products' : products
  }
  return render(request, 'store/products.html', context)

# show product
def show_product(request, product_id):
  try:
    product = Product.objects.get(id=product_id)
    title   = 'domein: ' + product.name
    context = {
      'title'   : title,
      'product' : product,
    }
    return render(request, 'store/show_product.html', context)
  except:
    raise Http404()

# orders
@login_required
def orders(request):
  title  = 'orders'
  orders = Order.objects.all()
  context = {
    'title'  : title,
    'orders' : orders
  }
  return render(request, 'store/orders.html', context)

# store
def store(request):
  title = 'store'
  data  = cartData(request)

  cartItems = data['cartItems']

  products = Product.objects.all()
  context = {
    'title'     : title,
    'products'  : products,
    'cartItems' : cartItems,
  }
  return render(request, 'store/store.html', context)

# cart
def cart(request):
  title = 'cart'
  data  = cartData(request)

  items     = data['items']
  order     = data['order']
  cartItems = data['cartItems']

  context = {
    'title'     : title,
    'items'     : items,
    'order'     : order,
    'cartItems' : cartItems
  }
  return render(request, 'store/cart.html', context)

# checkout
def checkout(request):
  title = 'checkout'
  data  = cartData(request)

  items     = data['items']
  order     = data['order']
  cartItems = data['cartItems']

  context = {
    'title'     : title,
    'items'     : items,
    'order'     : order,
    'cartItems' : cartItems
  }
  return render(request, 'store/checkout.html', context)

# update item in cart
def updateItem(request):
	data      = json.loads(request.body)
	productId = data['productId']
	action    = data['action']
	#print('Action :', action)
	#print('Product:', productId)

	customer           = request.user.customer
	product            = Product.objects.get(id=productId)
	order, created     = Order.objects.get_or_create(customer=customer, complete=False)
	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

# processOrder
def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp() # set unique transactionid
	data           = json.loads(request.body) # get submitted data
  # ingelogde user
	if request.user.is_authenticated:
		customer       = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
    # niet ingelogde user
		customer, order = guestOrder(request, data)
  # 
	total = float(data['form']['total'])
	order.transaction_id = transaction_id
  # check to prevent js hacking
	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer = customer,
		order    = order,
		address  = data['shipping']['address'],
		city     = data['shipping']['city'],
		state    = data['shipping']['state'],
		zipcode  = data['shipping']['zipcode'],
		country  = data['shipping']['country'],
		)
  
	return JsonResponse('Payment submitted..', safe=False)