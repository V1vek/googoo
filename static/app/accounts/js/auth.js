var accounts_url = base_url+'/accounts/';

var authHelpers = {
    setActiveAuthTab : function(active){
        $('.error_display').text('')
         var inactive = active == 'signin' ? 'signup' : 'signin'

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
    },
    afterRegister : function(response){
        $('.signup_form').removeAttr('disabled')
        if(response.message!=undefined){
            if(response.message.status=='success'){
                authHelpers.setActiveAuthTab('signin')
            }

            return;
        }
    },
    afterLogin : function(response){
        $('.signin_form').removeAttr('disabled')

        if(response.message!=undefined){
            if(typeof response.message.validation!='undefined' && response.message.validation.indexOf('verifi')!='-1'){
                 $('.error_display').html('<div>'+response.message.validation+' <span class="resend_verification"><a href="/accounts/resend_verification_email/">Resend verification email?</a></span></div>')

            }else{
                $('.error_display').text(response.message.validation)

            }
            $('input[name="password"]').val('')
            return;
        }
        if(response.token!=''){
           localStorage.setItem('jwt_token',response.token)
           window.location.reload()
        }

    },
    afterPasswordReset : function(response){
        $('.btn-reset-pwd').removeAttr('disabled')

        if(response.message!=undefined){
            $('.error_display').text(response.message)
            return;
        }
    },
    afterPasswordChange : function(response){
        $('.btn-reset-pwd').removeAttr('disabled')
        if(response.status=='success'){
//            window.location.href='/'
            $('.error_display').text(response.message)

        }else{
            $('.error_display').text(response.message)

        }
    }
}




    $('.resend_verification_form').validate({
       rules: {
            "email": {
                required: true,
                email: true
            },
       },
       submitHandler: function(form) {
            $('#resend-verification-email').attr('disabled','disabled')

            var data = {}
            $(form).serializeArray().map(function(x){data[x.name] = x.value;});
            helperMethods.ajaxHandler(accounts_url+'resend_email/','POST',data,function(response){
                $('#resend-verification-email').removeAttr('disabled')
                if(response.message!=undefined){
                    $('.error_display').text(response.message.validation)
                    return;
                }
            })
       }
    });

    $('.signin_form').validate({
       rules: {
            "email": {
                required: true,
                email: true
            },
            "password": {
                required: true,
            },
       },
       submitHandler: function(form) {
            $('.signin_form').attr('disabled','disabled')

            var data = {}
            $(form).serializeArray().map(function(x){data[x.name] = x.value;});
            helperMethods.ajaxHandler(accounts_url+'login_user/','POST',data,authHelpers.afterLogin)
       }
    });

    $('.signup_form').validate({
       rules: {
            "first_name": {
                required: true,
            },
            "last_name": {
                required: true,
            },
            "email": {
                required: true,
                email: true
            },
            "password" : {
                    required: true,
                    minlength : 6
                },
            "confirm_password" : {
                required: true,
                minlength : 6,
                equalTo : "#password"
            },
            "contact_number": {
                number: true,
                minlength : 8
            }
       },
       submitHandler: function(form) {
            $('.signup_form').attr('disabled','disabled')

            var data = {}

            $(form).serializeArray().map(function(x){

                data[x.name] = x.value;
            });

            helperMethods.ajaxHandler(accounts_url+'signup_user/','POST',data,authHelpers.afterRegister)
       }

    });

    $('.reset_password_form').validate({
       "password" : {
            required: true,
            minlength : 6
       },
       "confirm_password" : {
            required: true,
            minlength : 6,
            equalTo : "#password"
       },
       submitHandler: function(form) {
            $('.btn-reset-pwd').attr('disabled','disabled')
            var data = {}
            $(form).serializeArray().map(function(x){data[x.name] = x.value;});
            data['key'] = $('#reset-pwd').attr('data-key')

            console.log(data, $('#reset-pwd').attr('data-key'), $('.btn-reset-pwd'))

            helperMethods.ajaxHandler(accounts_url+'update_new_password/','POST',data,authHelpers.afterPasswordChange)
       }
    })

    $('.forgot_password_form').validate({
       rules: {
            "email": {
                email:true,
                required: true,
            },
       },
       submitHandler: function(form) {
            $('.btn-reset-pwd').attr('disabled','disabled')
            var data = {}
            $(form).serializeArray().map(function(x){data[x.name] = x.value;});
            helperMethods.ajaxHandler(accounts_url+'forgot_password/','POST',data,authHelpers.afterPasswordReset)
       }
    })



    $('.authentication').on('click',function(e){

        e.preventDefault();
        var active = $(this).attr('data-type');
        authHelpers.setActiveAuthTab(active)
    })

    $('.auth_tab').on('click',function(){
        var active = $(this).attr('data-type');
        authHelpers.setActiveAuthTab(active)
    })

    $('.forgot_password').on('click', function(){
        $('.error_display').text('')
         $('.forgot_password_tab').removeClass('hide')
         $('.forgot_password_form').removeClass('hide')
         $('.auth_tab').addClass('hide')
         $('.signin_form,signup_form').addClass('hide')
         $('.login-modal-center,.login-modal-right').addClass('hide')
    })

    $('#authentication-modal button.close').on('click', function(){
        $('.error_display').text('')
         $('.forgot_password_tab').addClass('hide')
         $('.forgot_password_form').addClass('hide')
         $('.auth_tab').removeClass('hide')
         $('.signin_form,signup_form').removeClass('hide')
         $('.login-modal-center,.login-modal-right').removeClass('hide')
    })

