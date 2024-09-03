// cart and product actions :

function add_to_cart(product_code, buttonelement) {
    var url = `http://127.0.0.1:8000/add_to_cart/${product_code}`

    $.ajax({
        url: url,
        type: 'GET',
        success: function (responseData) {
            alert(`${product_code} added to cart`);
        },
        error: function (xhr, status, error) {
            alert('some problem occured.');
        }
    });
}

function increase_cart_quantity(cart_id, price, buttonelement) {
    var url = `http://127.0.0.1:8000/increase_cart_quantity/${cart_id}`

    let parentDiv = buttonelement.parentElement;
    let span = parentDiv.querySelector('.quantity');

    if (span) {
        let quant = parseInt(span.textContent, 10) + 1;
        span.textContent = quant;
    }

    var curr_price = document.querySelector('#total_payable').innerText;
    curr_price = curr_price.slice(1);
    curr_price = parseInt(curr_price);
    var new_price = curr_price + parseInt(price);
    document.querySelector('#total_payable').innerHTML = `<b>₹${new_price}</b>`;

    var items = parseInt(document.querySelector('#total_items').innerText);
    items += 1;
    document.querySelector('#total_items').innerText = items;

    $.ajax({
        url: url,
        type: 'GET',
        success: function (responseData) {
            console.log(`increased`);
        },
        error: function (xhr, status, error) {
            alert('some problem occured.');
        }
    });
}

function decrease_cart_quantity(cart_id, price, buttonelement) {
    var url = `http://127.0.0.1:8000/decrease_cart_quantity/${cart_id}`

    let parentDiv = buttonelement.parentElement;
    let span = parentDiv.querySelector('.quantity');

    // if span is 1 then delete the cart product not decrease it and decrease the amount and item from the side bar.


    if (span) {
        let quant = parseInt(span.textContent, 10) - 1;
        span.textContent = quant;
    }


    var curr_price = document.querySelector('#total_payable').innerText;
    curr_price = curr_price.slice(1);
    curr_price = parseInt(curr_price);
    var new_price = curr_price - parseInt(price);
    document.querySelector('#total_payable').innerHTML = `<b>₹${new_price}</b>`;

    var items = parseInt(document.querySelector('#total_items').innerText);
    items -= 1;
    document.querySelector('#total_items').innerText = items;

    // alert(curr_price);

    $.ajax({
        url: url,
        type: 'GET',
        success: function (responseData) {
            console.log(`decreased`);
        },
        error: function (xhr, status, error) {
            alert('some problem occured.');
        }
    });
}
