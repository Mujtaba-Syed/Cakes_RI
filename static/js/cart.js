var updateBtns = document.getElementsByClassName('update-cart');

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var productId = this.getAttribute('data-product');
        var action = this.getAttribute('data-actions'); 
        console.log('productId:', productId, 'action:', action);
        console.log('USER: ', user);
        if (user == 'AnonymousUser') {
            addCookieItem(productId, action)
        } else {
            updateUserOrder(productId, action)
        }
    })
}

var cart = JSON.parse(getCookie('cart')) || {};  // Initialize cart if 'cart' is undefined

function addCookieItem(productId, action) {
    console.log('User Not logged in..');
    if (!cart[productId]) {
        cart[productId] = { 'quantity': 0 };
    }

    if (action == 'add') {
        cart[productId]['quantity'] += 1;
    } else if (action == 'remove') {
        cart[productId]['quantity'] = Math.max(0, cart[productId]['quantity'] - 1);
    }

    if (cart[productId]['quantity'] <= 0) {
        console.log('Item is Deleted');
        delete cart[productId];
    }

    console.log('cart: ', cart);
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
    // location.reload();
}
    // Assuming you want to perform the action on elements with specific IDs

    

function updateUserOrder(productId, action){
    // get div/element ids 

    console.log('User is authenticated, Sending data....');
    var url = '/update_item/';
    fetch(url,{
        method: 'POST', 
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId':productId, 'action':action})
    })
    .then((response)=>{
        window.location.reload(true); // Force a full page reload

        return response.json();
    })
    .then((data)=>{
        console.log('Data: ', data);
        // location.reload();
        updateCart(data)

    })
    .catch((error)=>{
        console.log('Error: ', error);
    });
}
function updateCart(data) {
    var cartElement = document.getElementById('cart');
    cartElement.innerHTML = 'Cart Items: ' + data.cartItems;

    var cartContainer = document.createElement('div');

    if (data.items.length > 0) {
        data.items.forEach(function (item) {
            var itemDiv = document.createElement('div');
            itemDiv.innerHTML = `
                <p>Product: ${item.product.name}</p>
                <p>Quantity: ${item.quantity}</p>
                <p>Total: $${item.get_total}</p>
            `;
            cartContainer.appendChild(itemDiv);
        });
    } else {
        cartContainer.innerHTML = '<p>Your cart is empty</p>';
    }

    cartElement.appendChild(cartContainer);

    alert('Cart updated successfully!');
}

