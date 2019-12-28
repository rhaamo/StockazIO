$("a.delete_link").click(function() {
    return confirm("Are you sure you want to delete this item ?");
});

$("span[class~=fi-minus-qty]").click(function() {
    // get current qty and calculate new qty
    var qty = parseInt($("span[class=qty]").html());
    if (qty == 0) {
        console.log("nope. i won't set -1 component. nope nope nope nope nope nope nope nope nope, oh wait, i missed the 80'th column, nooooo-");
        return;
    } // plz
    var new_qty = qty - 1;
    var id = $("span[class=component_id]").html();
    console.log("Setting comp (" + id + ") qty from " + qty + " to " + new_qty);

    // make call to change qty
    $.ajax({
        url: '/ajax/components/qty/change',
        type: 'GET',
        data: 'id=' + id + '&qty=' + new_qty,
        dataType: 'json',
        success : function(datas, status) {
            console.log(datas);
            $("span[class=qty]").html(datas.qty);
        }
    })
});

$("span[class~=fi-plus-qty]").click(function() {
    // get current qty and calculate new qty
    var qty = parseInt($("span[class=qty]").html());
    var new_qty = qty + 1;
    var id = $("span[class=component_id]").html();
    console.log("Setting comp (" + id + ") qty from " + qty + " to " + new_qty);

    // make call to change qty
    $.ajax({
        url: '/ajax/components/qty/change',
        type: 'GET',
        data: 'id=' + id + '&qty=' + new_qty,
        dataType: 'json',
        success : function(datas, status) {
            console.log(datas);
            $("span[class=qty]").html(datas.qty);
        }
    })
});

$("span[class~=fi-minus-order]").click(function() {
    // get current qty and calculate new qty
    var qty = parseInt($("span[class=order]").html());
    if (qty == 0) {
        console.log("nope. i won't set -1 order. nope nope nope nope nope nope nope nope nope, oh wait, i missed the 80'th column, nooooo-");
        return;
    } // plz
    var new_qty = qty - 1;
    var id = $("span[class=component_id]").html();
    console.log("Setting comp (" + id + ") order qty from " + qty + " to " + new_qty);

    // make call to change qty
    $.ajax({
        url: '/ajax/components/to_order/change',
        type: 'GET',
        data: 'id=' + id + '&qty=' + new_qty,
        dataType: 'json',
        success : function(datas, status) {
            console.log(datas);
            $("span[class=order]").html(datas.order_qty);
        }
    })
});

$("span[class~=fi-plus-order]").click(function() {
    // get current qty and calculate new qty
    var qty = parseInt($("span[class=order]").html());
    var new_qty = qty + 1;
    var id = $("span[class=component_id]").html();
    console.log("Setting comp (" + id + ") order qty from " + qty + " to " + new_qty);

    // make call to change qty
    $.ajax({
        url: '/ajax/components/to_order/change',
        type: 'GET',
        data: 'id=' + id + '&qty=' + new_qty,
        dataType: 'json',
        success : function(datas, status) {
            console.log(datas);
            $("span[class=order]").html(datas.order_qty);
        }
    })
});