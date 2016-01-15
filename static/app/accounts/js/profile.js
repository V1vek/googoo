$(document).ready(function(){
	var base_url = 'https://'+window.location.hostname;
	var api_url = base_url+'/api/';

	var userProfile = {

		profileSaved :  function(profile_type,response) {
		    $('#'+profile_type+'_profile .form-group').each(function(){
		        var input = $(this).find('input');
		        var span_el = $(this).find('span.'+profile_type+'_profile_value');
		        var value = input.val()
		        input.addClass('hide')
                $(this).find('.sp-dd').addClass('hide')
                $(this).find('.input-group-addon').addClass('hide')

                span_el.text(value)
		        span_el.removeClass('hide')

                if(profile_type=='seller'){
                    $('.estimate').addClass('width-sm-1').addClass('pad-top-zero').removeClass('pad-top-7')
                    $('.estimate_width').addClass('width-25').removeClass('width-40')
                    var val = $('#is_cod_available').is(':checked') ? 'available' : 'not available';
                    $('.seller_payment_option').text(val)
                    $('.shipping_free_amount').text($('input[name="shipping_free_amount"]').val())
                    var is_fulfilled = $('#is_textnook_fulfilled').is(':checked') ? '': 'Not';
                    $('.is_textnook_fulfilled').text(is_fulfilled)

                    $('span.estimate_from').text($('input.estimate_from').val())
                    $('span.estimate_to').text($('input.estimate_to').val())

		        }

		        $('#save_'+profile_type+'_profile').addClass('hide')
                $('#cancel_save_'+profile_type).addClass('hide')
                $('#edit_'+profile_type+'_profile').removeClass('hide')
                if($('#save_'+profile_type+'_profile').attr('data-method')=='POST'){
                    $('#save_'+profile_type+'_profile').attr('data-method','PUT')
                    if(typeof response.id!='undefined'){
                         $('#save_'+profile_type+'_profile').attr('data-id',response.id)

                    }
                }
		    })

		},
		afterImageUpload : function(response){
		    var type = response.type
		    if($('#save_'+type+'_profile').attr('data-method')=='POST'){
                $('#save_'+type+'_profile').attr('data-method','PUT')
            }
            $('#save_'+type+'_profile').attr('data-id',response.id)
            $('#'+type+'_pic_container').attr('src','')
            console.log(type,$('#'+type+'_pic_container').length)
            $('#'+type+'_pic_container').attr('src',response.image_url)
            if(type=='buyer'){
                 $('.user-img img').attr('src',response.image_url)
            }

            $('.avatar-pic img').attr('src',response.image_url)
		},
		passwordChanged : function(response){
		    $('#change_password input').each(function(){
		        $(this).val('')
		    })
            if(response.status=='error'){
                $('.error_display').text(response.validation)
            }else if(response.status="success"){
                $('.error_display').text(response.message)
            }
		}
	};


	$('.profile_tab').on('click',function(e){
        e.preventDefault()
        $('#page-content-wrapper .profile_content').each(function(){
            $(this).addClass('hide');
        })
        $('#page-content-wrapper .'+$(this).attr('data-tab')).removeClass('hide')
        $('.sidebar-nav li').removeClass('active')
        $(this).closest('li').addClass('active')
    })

      $("#menu-toggle").click(function(e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
      });

jQuery.validator.addMethod("nonNumeric", function(value, element) {
        console.log(this.optional(element) || !isNaN(Number(value)), !isNaN(Number(value)))
        return this.optional(element) || isNaN(Number(value));
    },"Only alphabatic characters allowed.");


	$('#seller_profile').validate({
       rules: {
            "first_name": {
                required: true,
            },
            "email": {
                required: true,
                email: true
            },
            "contact_number": {
                required: true,
                number: true,
                minlength : 8
            },
            "address": {
                required: true,
                nonNumeric: true
            },
            "city": {
                required: true,
            },
            "state": {
                required: true,
            },
            "zip_code": {
                required: true,
                number: true,
                minlength : 6
            }
       },
       submitHandler: function(form) {

            var data = {}
            $(form).serializeArray().map(function(x){
                if(x.name!='is_cod_available'){
                    if(x.value!=''){
                        data[x.name] = x.value;
                    }
                }


            });
            data['is_cod_available'] = $('#is_cod_available').is(':checked') ? true : false;
            data['is_textnook_fulfilled'] = $('#is_textnook_fulfilled').is(':checked') ? true : false;

            if(data['is_textnook_fulfilled']){
                data['shipping_fee']=0
                data['shipping_free_amount']=0

            }
            data['id'] = $('input#profile_id').val()
            data['username']=$('input#username').val()

            var method = $('#save_seller_profile').attr('data-method');

            ajax_url = method=='PUT' ? api_url+'sellers/'+$('#save_seller_profile').attr('data-id') : api_url+'sellers/'
            helperMethods.secureHTTPRequestHandler(ajax_url, method, data,function(response){
                userProfile.profileSaved('seller',response)
            })

       }

    });


    $('#buyer_profile').validate({
       rules: {
            "first_name": {
                required: true,
            },
            "email": {
                required: true,
                email: true
            },
            "contact_number": {
                required: true,
                number: true,
                minlength : 8
            },
            "address": {
                required: true,
                nonNumeric:true
            },
            "city": {
                required: true,
            },
            "state": {
                required: true,
            },
            "zip_code": {
                required: true,
                number: true,
                minlength : 6
            }
       },
       submitHandler: function(form) {
            var data = {}
            $(form).serializeArray().map(function(x){data[x.name] = x.value;});
            data['id'] = $('input#profile_id').val()
            data['username']=$('input#username').val()
            var method = $('#save_buyer_profile').attr('data-method');

            ajax_url = method=='PUT' ? api_url+'buyers/'+$('#save_buyer_profile').attr('data-id') : api_url+'buyers/'
            helperMethods.secureHTTPRequestHandler(ajax_url, method, data,function(response){
                userProfile.profileSaved('buyer',response)
            })

       }

    });


    $('#change_password').validate({
       rules: {
            "old_password": {
                required: true,
                minlength : 6,
            },
            "new_password": {
                required: true,
                minlength : 6,
            },
            "new_password1": {
                required: true,
                minlength : 6,
                equalTo : "#new_password"
            },

       },
       submitHandler: function(form) {
            var data = {}
            $(form).serializeArray().map(function(x){data[x.name] = x.value;});

            ajax_url = api_url+'accounts/change_password/'
            helperMethods.secureHTTPRequestHandler(ajax_url, 'POST', data, userProfile.passwordChanged)

       }

    });


    $('#edit_buyer_profile,#edit_seller_profile').on('click',function(){
        var this_el = $(this);
        var profie_type = this_el.attr('id').indexOf('buyer')>1 ? 'buyer' : 'seller';

        this_el.addClass('hide')

        $('#'+profie_type+'_profile .form-group').each(function(){
            var this_el = $(this);
            this_el.find('input').removeClass('hide')
            this_el.find('.input-group-addon').removeClass('hide')
            this_el.find('.sp-dd').removeClass('hide')

            this_el.find('.'+profie_type+'_profile_value').addClass('hide')
        })

        if(profie_type=='seller'){

            $('.estimate').removeClass('width-sm-1').removeClass('pad-top-zero').addClass('pad-top-7')
            $('.estimate_width').removeClass('width-25').addClass('width-40')
        }


        $('#save_'+profie_type+'_profile').removeClass('hide')
        $('#cancel_save_'+profie_type).removeClass('hide')

    })

    $('#cancel_save_buyer,#cancel_save_seller').on('click',function(){
        var this_el = $(this)
        var profie_type = this_el.attr('id').indexOf('buyer')>1 ? 'buyer' : 'seller'

        this_el.addClass('hide')

        $('#'+profie_type+'_profile .form-group').each(function(){
            var this_el = $(this);
            this_el.find('.input-group-addon').addClass('hide')
            this_el.find('input').addClass('hide')
            this_el.find('.sp-dd').addClass('hide')
            this_el.find('.'+profie_type+'_profile_value').removeClass('hide')
        })

        if(profie_type=='seller'){
            $('.estimate').addClass('width-sm-1').addClass('pad-top-zero').removeClass('pad-top-7')
            $('.estimate_width').addClass('width-25').removeClass('width-40')
        }


        $('#save_'+profie_type+'_profile').addClass('hide')
        $('#edit_'+profie_type+'_profile').removeClass('hide')
    })

    $('.upload_buyer_pic,.upload_seller_pic').on('click',function(e){
        var profie_type = $(this).attr('data-type');

        e.preventDefault();
        $('#'+profie_type+'_pic_input').trigger('click')
    })

    $('#buyer_pic_input').on('change',function(event){
        var file = document.getElementById("buyer_pic_input").files[0];
        var file_name=file.name
        var ext = file_name.substr(file_name.lastIndexOf('.')+1)
        if(ext!='png' && ext!='jpeg' && ext!='jpg'){
            return;
        }
        var url = api_url+'buyers/upload_image/'
        var fd = new FormData();
        fd.append("profile_image_url", file);
        helperMethods.secureHTTPRequestHandlerImage(url,'POST',fd, userProfile.afterImageUpload)
    })

    $('#seller_pic_input').on('change',function(event){
        var file = document.getElementById("seller_pic_input").files[0];
        var file_name=file.name
        var ext = file_name.substr(file_name.lastIndexOf('.')+1)
        if(ext!='png' && ext!='jpeg' && ext!='jpg'){
            return;
        }
        var url = api_url+'sellers/upload_image/'
        var fd = new FormData();
        fd.append("profile_image_url", file);
        helperMethods.secureHTTPRequestHandlerImage(url,'POST',fd, userProfile.afterImageUpload)
    })

     $('#renting_option').on('change',function(){
        var value = $(this).find("option:selected").text()
        $(this).closest('.form-group').find('span.seller_profile_value').text(value)

     })
    $('#selling_option').on('change',function(){
        var value = $(this).find("option:selected").text()
        $(this).closest('.form-group').find('span.seller_profile_value').text(value)

        if($(this).val()!='1'){
            $('.selling-options-group').removeClass('hide')
        }else{
           $('.selling-options-group').addClass('hide')
        }
        if($('.bsellOptions h3').length<1){
            $('.bsellOptions').prepend('<h3>'+value+'</h3>')
        }else{
            $('.bsellOptions h3').text(value)
        }
    })

    $('#book_condition').on('change', function(){
        var value = $(this).find("option:selected").text()
        $(this).closest('.form-group').find('span.seller_profile_value').text(value)
        if($('.bCondition h3').length<1){
            $('.bCondition').prepend('<h3>'+value+'</h3>')
        }else{
            $('.bCondition h3').text(value)
        }
    })

    $('.user_state').on('change', function(){
        var value = $(this).find("option:selected").text()
        $(this).closest('.form-group').find('span.prof_value').text(value)
        console.log('in')
    })

    $('#is_textnook_fulfilled').change(function(){
         $('input[name="shipping_free_amount"]').val('')
         $('input[name="shipping_fee"]').val('')

        if($('#is_textnook_fulfilled').is(':checked')){
            $('.shipping_option').addClass('hide')

        }else{
            $('.shipping_option').removeClass('hide')
        }

    })

    $('.submit-review').on('click', function(){
        var data={}
        $(this).attr('disabled','disabled')
        data['seller_id']=$(this).attr('data-seller-id')
        data['review'] = $('.seller-review').val()
        $(this).attr('disabled','disabled')
        $('textarea.seller-review').attr('disabled','disabled')
        ajax_url = base_url+'/api/seller/review/add/'
        helperMethods.secureHTTPRequestHandler(ajax_url, 'POST', data, function(response){
            console.log(response)
        })
    })

//    buyerProfile.ajaxHandler(base_url+'/accounts/token/','GET',{})
    $('.sellerRating input').on('click', function(e){
        e.preventDefault()
        var data = {}
        data['seller_id'] = $('.submit-review').data('seller-id')
        data['rating'] = $(this).val()

        ajax_url = base_url+'/api/seller/review/add/'
        helperMethods.secureHTTPRequestHandler(ajax_url, 'POST', data, function(response){

    })
})


})



