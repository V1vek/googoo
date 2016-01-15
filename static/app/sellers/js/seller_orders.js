var default_limit = 5
var order_index = default_limit
function formatDate(date){
    var d = new Date(date)
    var options = {
        year: "numeric", month: "short",
        day: "numeric", hour: "2-digit", minute: "2-digit"
    };
    var date = d.toLocaleTimeString("en-us", options)
    return date
}
var sellerDashboardOrders = {
    orderSearchResults: function(response){
    console.log(response.error!=undefined,response.error)
        if(response.error!=undefined){
            $('.load-orders').addClass('hide');
            return;
        }
        var response = JSON.parse(response)

        var order_template = _.template($('#order_tmpl').html());
        $('.tbody-order-table').append(order_template({"orders":response,'formatDate':formatDate}))

        if($('.tbody-order-table tr').length>=5){
            $('.load-orders').removeClass('hide');
        }else{
            $('.load-orders').addClass('hide');

        }
    },
}

$('.load-orders').on('click', function(){
    var order_status = $('.slt-order-filter').val()
    var params = order_status=='' ? 'index='+order_index : 'index='+order_index+'&order_status='+order_status
    var url = base_url+'/api/load_more_order/sellers/?'+params
    helperMethods.secureHTTPRequestHandler(url,'GET',{}, sellerDashboardOrders.orderSearchResults)
    order_index+=default_limit;
})

$('.slt-order-filter').on('change', function(){
    order_index = 0
    var order_status = $('.slt-order-filter').val()
    var params = order_status=='' ? 'index='+order_index : 'index='+order_index+'&order_status='+order_status
    var url = base_url+'/api/load_more_order/sellers/?'+params

    helperMethods.secureHTTPRequestHandler(url,'GET',{}, function(response){
        if(response.error!=undefined){
            $('.order-table').addClass('hide')
            $('.no-order-results').removeClass('hide')
            $('.load-orders').addClass('hide')
        }else{
            $('.order-table').removeClass('hide')
            $('.no-order-results').addClass('hide')
            $('.tbody-order-table').html('')
        }
        sellerDashboardOrders.orderSearchResults(response)
    })
    order_index+=default_limit;
})