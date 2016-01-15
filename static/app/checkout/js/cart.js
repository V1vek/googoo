$(document).ready(function() {

    var cart = {
        addedToCart : function(el, response){
            //window.location.href='/orders/
            if(response.status==302){

                var inactive = 'signup'
                var active = 'signin'

                $('#authentication-modal').modal('show');

                $('#authentication-modal .'+active+'_form').removeClass('hide')
                $('#authentication-modal .'+inactive+'_form').addClass('hide')

                $('.'+active+'_tab').addClass('active')
                $('.'+inactive+'_tab').removeClass('active')

                if(active=='signin'){
                    $('.login-modal-center').addClass('hr-signin')
                }else{
                    $('.login-modal-center').removeClass('hr-signin')
                }

                return;
            }
            el.html('<h4>Added to cart</h4>')
            $('.shopping-item').text(response.quantity)

            var counter = 0;
            var timer;
             timer = setInterval(function(){
                $('.shopping-item').toggleClass("shoppingBlink");
                 if(counter>6){
                     clearInterval(timer)
                 }
                 counter+=1
             },200)
        },
        cartQuantityUpdated : function (response, el){

            if (response.cart!=undefined){

                var cart = response.cart
                var el = el.closest('.check-bookInfo')
                el.find('.cBook-sp').html('<i class="fa fa-rupee"></i> '+cart['item_selling_price'])
                el.find('.orgnl-rate').html('<i class="fa fa-rupee"></i> '+cart['item_price'])
                el.find('.book_quantity').val(cart['quantity'])
                $('.cBH-amount').html('Total:<i class="fa fa-rupee"></i>'+cart['cart_total'])
                $('.cart_total').text(cart['cart_total'])
                $('.shipping_price').text(cart['shipping_price'])
                $('.total_value').text(cart['total'])
                $('.checkout_cart_total').text(cart['cart_total'])
                $('.discount_price').text(cart['discount_price'])
                $('.checkout_shipping_price').text(cart['shipping_price'])
                $('.checkout_total_value,.payable_total').text(cart['total'])
                if(cart['total']<10){
                   $('.payment-btn').addClass('hide')
                   $('.cod-btn').addClass('hide')
                   $('.free-btn').removeClass('hide')

                }
            }
        },
        afterCartItemRemoved : function(response,el){


            if (response.cart!=undefined){

                el.closest('.checkout-BD-holder').remove()
                if($('.checkout-BD-holder').length<1){
                    $('.checkout-content-right').addClass('hide')
                    $('.empty-cart').removeClass('hide')
                }

                $('.cart_count').text(parseInt($('.cart_count').text())-1)

                var cart = response.cart
                $('.cBH-amount').html('Total:<i class="fa fa-rupee"></i>'+cart['cart_total'])
                $('.cart_total').text(cart['cart_total'])
                $('.shipping_price').text(cart['shipping_price'])
                $('.total_value').text(cart['total'])
                $('.checkout_cart_total').text(cart['cart_total'])
                $('.checkout_shipping_price').text(cart['shipping_price'])
                $('.checkout_total_value,.payable_total').text(cart['total'])
                $('.discount_price').text(cart['discount_price'])

                if(cart['total']<10){
                   $('.payment-btn').addClass('hide')
                   $('.cod-btn').addClass('hide')
                   $('.free-btn').removeClass('hide')

                }

                if(cart['is_cod_available']){
                    $('.cod-btn').removeAttr('disabled')
                    $('.cod-text').addClass('hide')
                }else{
                    $('.cod-btn').attr('disabled','disabled')
                    $('.cod-text').removeClass('hide')
                }
            }
        },
        generateInstaMojoLink : function(){
              data = {

              }
              helperMethods.secureHTTPRequestHandler(cart_url, 'POST', data, cart.addedToCart)
        },
        orderInitiated :  function(response){
            $('#order_id').val(response.order_id)

            if(cart['total']<10){
               $('.payment-btn').addClass('hide')
               $('.cod-btn').addClass('hide')
               $('.free-btn').removeClass('hide')

            }

        },
        createInstaMojoLink : function(response){

             var pg_link = base_url+'/api/instamojo/link/'
             helperMethods.secureHTTPRequestHandler(pg_link, 'POST', data, cart.afterLinkCreated)

        },
        afterLinkCreated : function(response){
            if(response.url!=undefined){

                $('.cS-num').removeClass('active');
                $('.step-3').addClass('active')
                $('.shipment_container').addClass('hide')
                $('.payment_container').removeClass('hide')
                $('.shp-payment-form iframe').attr('src',response.url)
            }
        }

    }


     $('.buy_now,.rent_now').on('click',function(e){
        var el = $(this).parent()
        e.preventDefault()
        var cart_url = base_url+'/api/cart/add/'
        data = {
            'book_id': $(this).attr('data-book-id'),
            'seller_id':$(this).attr('data-seller-id'),
            'quantity':1,
            'seller_book_condition_id':$(this).attr('data-seller-book-condition-id'),
            'renting_options': $(this).attr('data-type')=='rent' ? '1' : '2'
        }
        helperMethods.secureHTTPRequestHandler(cart_url, 'POST', data, function(response){
            cart.addedToCart(el,response)
        })
     })


    $(".filter").click(function(event){
        event.preventDefault();
        $("#Msearch").slideToggle("slow");
        $('.tabpanel').slideToggle("slow");
    });


    $(".p-search-cat-list").mCustomScrollbar();

    $('.p-search-var-items input:radio').screwDefaultButtons({
       image: 'url("/static/main/images/radio_button.png")',
       width: 14,
       height: 14
    });

    $('.save_quantity').on('click', function(){
        var cart_url = base_url+'/api/cart/update/'
        var el = $(this)
        data = {
            'quantity':el.closest('.cBook-quantity').find('.book_quantity').val(),
            'cart_id':el.data('cart-id'),
        }

        helperMethods.secureHTTPRequestHandler(cart_url, 'POST', data, function(response){
            cart.cartQuantityUpdated(response, el)
        })

    })

    $('.shop-cart').on('click', function(){
        if($.trim($('.shopping-item').text())!='0'){
            window.location.href='/orders/checkout/'
        }
    })



    $('.cBook-remove').on('click', function(e){
        e.preventDefault();
        var el =$(this)
        var cart_id = el.attr('data-cart-id')
        var cart_url = base_url+'/api/cart/remove/'
        data = {
            'cart_id':cart_id,
        }
        helperMethods.secureHTTPRequestHandler(cart_url, 'POST', data, function(response){
            cart.afterCartItemRemoved(response,el)
        })

    })

    $('.placeOrder').on('click', function(){

        if(parseFloat($('.total_value').text())<10){
            $('.payment-btn').addClass('hide')
            $('.cod-btn').addClass('hide')
            $('.free-btn').removeClass('hide')
        }

        $('.cS-num').removeClass('active');
        $('.step-2').addClass('active')
        $('.step-1').attr('data-enabled','true')
        $('.step-2').attr('data-enabled','true')
        $('.checkout_container').addClass('hide')
        $('.shipment_container').removeClass('hide')

        var cart_url = base_url+'/api/orders/'

        data = {
            'order_options' : '1'
        }

        helperMethods.secureHTTPRequestHandler(cart_url, 'POST', data, function(response){
            cart.orderInitiated(response)
        })

    })

    function validate_shipping_address(callback){
        if($.trim($('.shp-address').attr('data-valid'))=='true'){

              if($.trim($('.shp-address').attr('data-type'))=='buyer_address'){
                var data = {}
                $('.shp-address .details').each(function(){
                    data[$(this).data('id')] = $.trim($(this).text())
                })

                data['user_id'] = $('#user_id').val()
                data['order_id'] = $('#order_id').val()

                ajax_url = base_url+'/api/shipping_addresses/'
                helperMethods.secureHTTPRequestHandler(ajax_url, 'POST', data, callback)


              }else{
                callback()
              }

        }
    }

    $('.continuePayment').on('click', function(){
        validate_shipping_address(cart.createInstaMojoLink)

    })

    $('.confirmCod').on('click', function(){
         validate_shipping_address(function(){
            window.location.href="/orders/paid/?payment_mode=cod"
         })
    })

    $('.cod-btn').on('click', function(){
         $('#codValid').modal('show')
    })

    $('.free-btn').on('click', function(){
         validate_shipping_address(function(){
            window.location.href="/orders/paid/?payment_mode=free"
         })
    })

    $('.cS-num').on('click',function(){
        if($(this).hasClass('step-3')){
            return;
        }
        if($(this).attr('data-enabled')=='true'){
            $('.cS-num').removeClass('active')
            $(this).addClass('active')
            $('.checkout').addClass('hide')
            $('.'+$(this).data('type')).removeClass('hide')
        }
    })


    $('.discount_coupon').on('submit', function(e){
        e.preventDefault();
        var data = {}
        data['coupon_code'] = $('#coupon_code').val()
        if(data['coupon_code']==''){
            $('#coupon_code-error').removeClass('hide')
            return
        }else{
            $('#coupon_code-error').addClass('hide')
        }
        ajax_url = base_url+'/api/coupon/apply/';
        helperMethods.secureHTTPRequestHandler(ajax_url, 'POST', data, function(response){
            if(response.success!=undefined){
                $('.cBook-coupon').addClass('hide')
                $('.coupon_code').removeClass('hide')
                $('.applied_coupon').text(response.coupon_code)
                $('.total_value').text(response.cart_values['total'])
                $('.checkout_cart_total').text(response.cart_values['cart_total'])
                $('.discount_price').text(response.cart_values['discount_price'])
            }
        })

    })

    $('.remove_coupon').on('click', function(){
        var data = {}
        data['coupon_code'] = $.trim($('.applied_coupon').text())

        ajax_url = base_url+'/api/coupon/remove/';
        helperMethods.secureHTTPRequestHandler(ajax_url, 'POST', data, function(response){
            if(response.success!=undefined){
                $('.cBook-coupon').removeClass('hide')
                $('.coupon_code').addClass('hide')
                $('.applied_coupon').text('')
                $('.total_value').text(response.cart_values['total'])
                $('.checkout_cart_total').text(response.cart_values['cart_total'])
                $('.discount_price').text(response.cart_values['discount_price'])
            }
        })

    })

    $('.cBook-collap').on('click', function(){
        if($(this).closest('.check-bookInfo').find('.cBook-footer').attr('data-open')=='false'){
            $(this).closest('.check-bookInfo').find('.cBook-footer').css('display','block')
            $(this).closest('.check-bookInfo').find('.cBook-footer').attr('data-open','true')
        }else{
          $(this).closest('.check-bookInfo').find('.cBook-footer').attr('data-open','false')
          $(this).closest('.check-bookInfo').find('.cBook-footer').css('display','none')
        }
    })




});