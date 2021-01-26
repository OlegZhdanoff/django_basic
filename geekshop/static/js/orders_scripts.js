window.onload = function () {
    let _quantity, _price, orderitem_num, delta_quantity, orderitem_quantity, delta_cost;
    let quantity_arr = [];
    let price_arr = [];

    let TOTAL_FORMS = parseInt($('input[name=orderitems-TOTAL_FORMS]').val());
    let order_total_quantity = parseInt(($('.order_total_quantity')).text()) || 0;
    let order_total_price = parseFloat(($('.order_total_cost')).text().replace(',', '.')) || 0;

    for(let i=0; i<TOTAL_FORMS; i++) {
        _quantity = parseInt($('input[name=orderitems-' + i + '-quantity]').val());
        _price = parseFloat($('span.orderitems-' + i + '-price').text().replace(',', '.'));

        quantity_arr[i] = _quantity;
        if (_price){
            price_arr[i] = _price;
        } else {
            price_arr[i] = 0;
        }
    }
    // console.log(quantity_arr);
    // console.log(price_arr);
    $('.order_form').on('click', 'input[type=number]', function () {
        let target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));
        if(price_arr[orderitem_num]) {
            orderitem_quantity = parseInt(target.value);
            delta_quantity = orderitem_quantity - quantity_arr[orderitem_num];
            quantity_arr[orderitem_num] = orderitem_quantity;
            orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
        }
    });
    $('.order_form').on('click', 'input[type=checkbox]', function () {
        let target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-DELETE', ''));
        if(target.checked) {
            delta_quantity = -quantity_arr[orderitem_num];
            console.log('id_orderitems-' + orderitem_num + '-quantity');
            // ($('input[name=orderitems-' + orderitem_num + '-quantity]')).disabled = true;
            document.getElementById('id_orderitems-' + orderitem_num + '-quantity').disabled = true;
            console.log(($('input[name=orderitems-' + orderitem_num + '-quantity]')).disabled);

        } else {
            delta_quantity = quantity_arr[orderitem_num];
             document.getElementById('id_orderitems-' + orderitem_num + '-quantity').disabled = false;
            $('#id_orderitems-' + orderitem_num + '-quantity').disabled = false;
        }
        orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
    });

    function orderSummaryUpdate(orderitem_price, delta_quantity) {
        delta_cost = orderitem_price * delta_quantity;
        order_total_price = Number((order_total_price + delta_cost).toFixed(2));
        order_total_quantity = order_total_quantity + delta_quantity;

        $('.order_total_quantity').html(order_total_quantity.toString());
        $('.order_total_cost').html(order_total_price.toString());
    }
}