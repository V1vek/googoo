 $('.btn-fullfill-order').on('click', function(){
    $('#fulfill_order').modal('show')
    $('#fulfill_order #order_status option[value="5"]').remove()
    $('#fulfill_order #tracking_id').val('')
    $('#fulfill_order #tracking_url').val('')
    $('.save_order_details').attr('data-type','order-seller')
})

var order_status = ['processed', 'cancelled', 'shipped', 'delivered', 'received']
$('.save_order_details').on('click', function(){

    var type = $(this).data('type')
    data = {}
    data['order_status'] = $('.fulfill_order_form #order_status').val()

    if(type=='order-seller'){

        data['order_seller_id'] = $(this).data(type+'-id')
        var ajax_url = base_url+'/api/seller_order_details/change/'
        $('.order-table .order_status').each(function(){
            $(this).text(order_status[parseInt($('#fulfill_order #order_status').val())-1])
        })

    }else if(type=='order-item'){

        data['order_item_id'] = $(this).data(type+'-id')
        var ajax_url = base_url+'/api/seller/order_item_details/change/'
        $('.order-table tr td i.edit_order_seller[data-order-item-id="'+data['order_item_id']+'"]')
        .closest('tr').find('.order_status').text(order_status[parseInt(data['order_status'])-1])
    }

    data['tracking_id'] = $('.fulfill_order_form #tracking_id').val()
    data['tracking_url'] = $('.fulfill_order_form #tracking_url').val()

    helperMethods.secureHTTPRequestHandler(ajax_url, 'POST', data, function(response){
        console.log(response)
    })

})

$('.edit_order_seller').on('click', function(){
    var order_item_id = $(this).attr('data-order-item-id')
    var self = this;
    var ajax_url = base_url+'/api/order_item_details/?order_item_id='+order_item_id+'&sender=seller'

    helperMethods.secureHTTPRequestHandler(ajax_url, 'GET', {}, function(response){
        var tracking_id = response.tracking_id != undefined ? response.tracking_id : '-'
        var tracking_url = response.tracking_url != undefined ? response.tracking_url: '-'
        var order_status = response.order_status != undefined ? response.order_status : '1'
        $('#fulfill_order').modal('show')
        $('.save_order_details').attr('data-order-item-id', $(self).data('order-item-id'))
        $('.save_order_details').attr('data-type','order-item')
        $('#fulfill_order #tracking_id').val(tracking_id)
        $('#fulfill_order #tracking_url').val(tracking_url)

        if(order_status=='3'){
           $('#fulfill_order #order_status option[value="1"]').remove()
           $('#fulfill_order #order_status option[value="2"]').remove()
           $('#order_status').append('<option value="5">Received</option>')
        }

        $('#fulfill_order #order_status').val(order_status)

    })

})



$('.edit_order_item').on('click', function(){

    var order_item_id = $(this).attr('data-order-item-id')

    var ajax_url = base_url+'/api/order_item_details/?order_item_id='+order_item_id+'&sender=buyer'

    helperMethods.secureHTTPRequestHandler(ajax_url, 'GET', {}, function(response){

        var tracking_id = response.tracking_id != undefined ? response.tracking_id : '-'
        var tracking_url = response.tracking_url != undefined ? response.tracking_url : '-'
        $('#order_item_details').modal('show')
        $('#order_item_details #tracking_id').text(tracking_id)
        $('#order_item_details #tracking_url').text(tracking_url)
        $('#order_item_details .request_order_cancellation').attr('data-id',response.id)

        if(response.order_status!='1'){
            $('#order_item_details .request_order_cancellation').attr('disabled','disabled')
        }else{
            $('#order_item_details .request_order_cancellation').removeAttr('disabled')
        }

    })

})



$('.request_order_cancellation').on('click',function(){
    $('#cancel_order_modal').modal('show')
    $('#cancel_order_modal .cancel_order').attr('data-id',$(this).attr('data-id'))
})

$('.cancel_order').on('click', function(){
    var order_item_id = $(this).attr('data-id')
    var ajax_url = base_url+'/api/buyer/order_item_details/change/';

    helperMethods.secureHTTPRequestHandler(ajax_url, 'POST', {'order_item_id':order_item_id}, function(response){
        $('.order-table tr td i.edit_order_item[data-order-item-id="'+order_item_id+'"]')
        .closest('tr').find('.order_status').text('Cancelled')
    })
})

$('.order_tab').on('click', function(e){
   e.preventDefault()
   $('.order-right div.right_container').addClass('hide')
   $('.'+$(this).attr('id')).removeClass('hide')
})

$('.submit-notes').on('click', function(){
    var note = $('.order_note').val()
    var order_id = $(this).data('order-id')
    if(note!=''){
       $(this).attr('disabled','disabled')
           var ajax_url = base_url+'/api/order_notes/'
           helperMethods.secureHTTPRequestHandler(ajax_url, 'POST', {'note':note,'order_id':order_id}, function(response){
                $('.order_note').val('')
                $('.submit-notes').removeAttr('disabled')
                if(response.note==undefined){
                    return
                }
                var d = new Date(response.date)
                var options = {
                    year: "numeric", month: "short",
                    day: "numeric", hour: "2-digit", minute: "2-digit"
                };
                var date = d.toLocaleTimeString("en-us", options)
                $('.order_notes').append('<div class="order-history-details"><p>'+date+'</p><p>'+response.note+'</p></div>')
           })
    }

})

$('.email_buyer').on('click', function(){
    var email = $('.buyer-email').val()
    var order_id = $(this).data('order-id')
    console.log(order_id)
    if(email!=''){
        $(this).attr('disabled','disabled')
        var ajax_url = base_url+'/api/send_email/buyer/'
        helperMethods.secureHTTPRequestHandler(ajax_url, 'POST', {'email':email,'order_id':order_id}, function(response){
           $('.email_buyer').removeAttr('disabled')

        })

    }
})

$('#order_status').on('change', function(){
    if($(this).val()=='1'){
        $('.track').removeClass('hide')
        $('.btn-fullfill-order').text('FULFILL ORDER')
        $('.order-desc').text('YOU NEED TO FULL FILL ORDER')
        $('.btn-fullfill-order').removeAttr('disabled')
    }
    if($(this).val()=='2'){
        $('.track').removeClass('hide')
        $('.btn-fullfill-order').text('ORDER CANCELLED')
        $('.order-desc').text('ORDER HAS BEEN CANCELLED')
        $('.btn-fullfill-order').attr('disabled','disabled')
    }
    if($(this).val()=='3'){
        $('.track').removeClass('hide')
        $('.btn-fullfill-order').text('ORDER FULFILLED')
        $('.btn-fullfill-order').attr('disabled','disabled')
        $('.order-desc').text('ORDER HAS BEEN SHIPPED')

    }else{
        $('.track').addClass('hide')
        $('.track').each(function(){
            $(this).find('input').val('')
        })
    }
})

$('.print_order_summary').on('click', function(e){
     e.preventDefault()
     var printContents = document.querySelector('.s-order-summary').innerHTML;
     var originalContents = document.body.innerHTML;
     document.body.innerHTML = printContents;
     window.print();
     window.location.reload()
})