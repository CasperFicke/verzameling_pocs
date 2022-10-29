// store/static/store/scripts/store.js

// maak list van alle buttons met classname update-cart
var updateBtns = document.getElementsByClassName('update-cart')

// loop door de list van buttons en zet een eventlister op de click
for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action    = this.dataset.action
		console.log('productId:', productId, 'Action:', action)
		console.log('USER:', user)
    // update cart
		if (user == 'AnonymousUser'){
      // update for not loggedin user
			addCookieItem(productId, action)
		} else {
      // update for loggedin user
			updateUserOrder(productId, action)
		}
	})
}

// function to update cart for not loggedin user  (in the cookie)
function addCookieItem(productId, action){
	console.log('User is not authenticated')
  // toevoegen
	if (action == 'add'){
		if (cart[productId] == undefined){
		cart[productId] = {'quantity':1}
		} else {
			cart[productId]['quantity'] += 1
		}
	}
  // verwijderen
	if (action == 'remove'){
		cart[productId]['quantity'] -= 1
		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + "; domain=;path=/;  SameSite=None; Secure"
	location.reload()
}

// function to update cart for loggedin user by sending productId en action to the backend (updateItem view)
function updateUserOrder(productId, action){
	console.log('User is authenticated, sending data...')
		var url = '/store/update_item/'
    // 
		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type': 'application/json',
				'X-CSRFToken' : csrftoken,
			}, 
			body:JSON.stringify({'productId':productId, 'action':action})
		})
		.then((response) => {
		  return response.json();
		})
		.then((data) => {
      console.log('data: ', data)
		  location.reload() // reload the page
		});
}