# store/utils.py

# django
import json

# local
from .models import Customer, Product, Order, OrderItem

# cookieCart;
# function with logic needed for maintaining a cart for a non-logged in user in a cookie
def cookieCart(request):
	#Create empty cart for now for non-logged in user
	try:
		cart = json.loads(request.COOKIES['cart'])
	except:
		cart = {}
	# print('CART:', cart)

	items = []
	order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
	cartItems = order['get_cart_items']
  # update items counter
	for i in cart:
		# try block to prevent items in cart that may have been removed from causing error
		try:	
			if(cart[i]['quantity']>0): #items with negative quantity = lot of freebies  
				cartItems += cart[i]['quantity']
        # calc productprice on this order
				product = Product.objects.get(id=i)
				total = (product.price * cart[i]['quantity'])
        # calc total price of order
				order['get_cart_total'] += total
        # calc total number of order items
				order['get_cart_items'] += cart[i]['quantity']
        # put output into datamodel
				item = {
				'id'       : product.id,
				'product'  : {
          'id'       : product.id,
          'name'     : product.name,
          'price'    : product.price,
				  'imageURL' : product.imageURL,
        },
        'quantity' : cart[i]['quantity'],
				'digital'  : product.digital,'get_total':total,
				}
				items.append(item)
        # check for only digital products
				if product.digital == False:
					order['shipping'] = True
		except:
			pass
			
	return {
    'cartItems' : cartItems,
    'order'     : order,
    'items'     : items
  }

# cartData;
# function with logic needed for splitting between loggedin and non-loggedin user
def cartData(request):
  if request.user.is_authenticated:
    # loggedin user
    customer       = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items          = order.orderitems.all()
    cartItems      = order.get_cart_items
  else:
    # non-loggedin user
    cookieData = cookieCart(request)
    cartItems  = cookieData['cartItems']
    order      = cookieData['order']
    items      = cookieData['items']
  return {
    'cartItems' : cartItems,
    'order'     : order,
    'items'     : items
  }

# Function with logic to handle a non-loggedin user order
def guestOrder(request, data):
	name       = data['form']['name']
	email      = data['form']['email']
	cookieData = cookieCart(request)
	items      = cookieData['items']
  # create new customer or add to existing customer is email exists
	customer, created = Customer.objects.get_or_create(
			email=email,
			)
	customer.name = name
	customer.save()
  # create order
	order = Order.objects.create(
		customer = customer,
		complete = False,
		)
  # loopthrough itemlist in the cookie and add them to the database
	for item in items:
		product   = Product.objects.get(id=item['id'])
		orderItem = OrderItem.objects.create(
			product  = product,
			order    = order,
			quantity = (item['quantity'] if item['quantity']>0 else -1*item['quantity']), # negative quantity = freebies
		)
	return customer, order