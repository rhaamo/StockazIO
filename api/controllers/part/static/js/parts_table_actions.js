/**
 * Created by dashie on 19/10/15.
 */

$('#contentBody')
    .on("click", ".part_row", function () {
        var row = $(this);

        // make table col-lg-9
        document.getElementById('ContentTableParts').className = "col-md-9 withSidebar";

        // make sidebar col-lg-3
        document.getElementById('ContentPartSidebar').className = "col-md-3 opened";

        // load sidebar content
        $('#ContentPartSidebar').load('/ajax/parts/' + row.data().id + '/sidebar', function () {
            //alert("ok");
        });
    })
    .on("click", ".del", function () {
        var item = $(this);
        var id = $(this).parent().parent().data().id;
        var item_name = $(this).data().name;
        if (!confirm("Are you sure to delete " + item_name + " ?")) {
            return false;
        }

        $.ajax({
            url: '/parts/' + id + '/del',
            type: 'DELETE',
            success: function (result) {
                item.parent().parent().remove()
            }
        });

        return false;
    })
    .on("click", ".aj_stock_minus", function () {
        var item = $(this);
        var id = $(this).parent().parent().data().id;

        $.ajax({
            url: '/ajax/parts/' + id + '/stock/dec',
            type: 'POST',
            success: function (result) {
                $("#aj_stock_" + id).html(result.Record.StockLevel);
                $("#aj_min_stock_" + id).html(result.Record.MinStockLevel);
            }
        });

        return false;
    })
    .on("click", ".aj_stock_plus", function () {
        var item = $(this);
        var id = $(this).parent().parent().data().id;

        $.ajax({
            url: '/ajax/parts/' + id + '/stock/inc',
            type: 'POST',
            success: function (result) {
                $("#aj_stock_" + id).html(result.Record.StockLevel);
                $("#aj_min_stock_" + id).html(result.Record.MinStockLevel);
            }
        });

        return false;
    });