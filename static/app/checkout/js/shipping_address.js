var shipping_address = {
    addressUpdated : function(response){
        if (typeof response.data == undefined){
            return;
        }
        var response = response.data
        $('.shp-address .details').each(function(){
              console.log(response[$(this).data('id')])

            $(this).text(response[$(this).data('id')])
        })

        $('#shipping_address').modal('hide')

    }
}

$('.btn-save-address').on('click', function(){

    $('.shipping_address').validate({
       rules: {
            "name": {
                required: true,
            },
            "address": {
                required: true,
            },
            "state": {
                required: true,
            },
            "zip_code": {
                required: true,
                minlength : 6,
            },
            "contact_number": {
                required: true,
                minlength : 6,
            },
            "city": {
                required: true,
            },

       },
       submitHandler: function(form) {
            var data = {}
            $(form).serializeArray().map(function(x){data[x.name] = x.value;});
            console.log(data)
            ajax_url = base_url+'/api/shipping_addresses/'
            helperMethods.secureHTTPRequestHandler(ajax_url, 'POST', data, shipping_address.addressUpdated)

       }

    });
})


 $('.shp-edit').on('click', function(e){
    e.preventDefault()
    $('#shipping_address').modal('show')

})