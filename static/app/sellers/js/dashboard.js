var sellerDashboard = {
    inventorySearchResults: function(response){
        var response = JSON.parse(response)
        var inventory_template = _.template($('#inventory_tmpl').html());
        $('.inventory-table tbody').remove()
        $('.inventory-table').append(inventory_template({'inventories':response}))
        if($('.inventory-table .it-section').length>=5){
            $('.load-more-inventory').removeClass('hide');
        }else{
            $('.load-more-inventory').addClass('hide');

        }

    },

    renderInventory: function(response){

        if(response.error!=undefined){
            $('.load-more-inventory').addClass('hide');
            return
        }
        var response = JSON.parse(response)
                console.log(response)

        var inventory_template = _.template($('#inventory_tmpl').html());
        $('.inventory-table').append(inventory_template({'inventories':response}))

        if($('.inventory-table .it-section').length>=5){
            $('.load-more-inventory').removeClass('hide');
        }else{
            $('.load-more-inventory').addClass('hide');
        }

    },

    removedInventory : function(el){
       if(el.closest('tbody').find('tr.it-sec-tr').length>1){
            el.closest('tr').remove();
       }else{
            el.closest('tbody').remove()
       }
       if($('.inventory-table tbody tr').length<1){
            $('.inventory-details-container').addClass('hide')
       }
    },
}

var default_limit = 5
 var inventory_index = default_limit

$('.search-inventory').on('keyup', function(){
    var self = this
    delay(function(){
        var keyword = $(self).val()

            var url = base_url+'/api/sellers/books/?keyword='+keyword
            helperMethods.secureHTTPRequestHandler(url,'GET',{}, sellerDashboard.inventorySearchResults)
            inventory_index = default_limit
    }, 600 )

 })


$(document).on('click','.tclose-desktop', function(e){
    e.preventDefault();
    var inventory_id = $(this).attr('id')
    $('.delete_inventory').attr('data-inventory-id',inventory_id)
    $('#bookInventory').modal('show')



})

$('.delete_inventory').on('click',function(){
    var inventory_id = $('.delete_inventory').attr('data-inventory-id')
    var el = $('#'+inventory_id)
    var seller_book_condition_id = el.data('id')
    var seller_book_id = el.data('seller-book-id')

    var url = '/api/sellers/books/remove/'
    helperMethods.secureHTTPRequestHandler(url,'POST',{'seller_book_id':seller_book_id,'seller_book_condition_id' : seller_book_condition_id})

    sellerDashboard.removedInventory(el)
})

 $('.load-more-inventory').on('click', function(){
    var keyword = $('.search-inventory').val()
    var params = keyword=='' ? 'index='+inventory_index : 'index='+inventory_index+'&keyword='+keyword
    var url = base_url+'/api/sellers/books/?'+params
    helperMethods.secureHTTPRequestHandler(url,'GET',{}, sellerDashboard.renderInventory)
    inventory_index+=default_limit;
 })


 $('.inventory-display,.order-display').on('click', function(e){
    e.preventDefault();
    var type = $(this).data('type')
    if($(this).attr('data-open')=='false'){
        $('.'+type+'-details-container').hide('slide',{direction:'up'},600)
        $(this).attr('data-open','true')
        $(this).removeClass('up-arrow')
        $(this).addClass('down-arrow')

    }else{
        $('.'+type+'-details-container').show('slide',{direction:'up'},600)
        $(this).attr('data-open','false')
        $(this).addClass('up-arrow')
        $(this).removeClass('down-arrow')

    }

 })