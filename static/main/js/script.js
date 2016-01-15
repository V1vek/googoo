var base_url = 'http://'+window.location.hostname;


var helperMethods = {

    ajaxHandler : function(url,method,data,callback){
        var ajax_data = {
            'url':url,
            'type':method,
            'data':data,
            'success':function(response){
                if(typeof callback!='undefined' && response){
                    callback(response)

                }
            }
        }

        var csrf_token = helperMethods.getCookie('csrftoken');
        if(csrf_token!=''){
            ajax_data['beforeSend'] = function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }

        $.ajax(ajax_data)
    },
    ajaxHandlerJWTImage : function(url,method,data,token,callback){

        var csrf_token = helperMethods.getCookie('csrftoken');

        $.ajax({
            'url':url,
            'type':method,
            'data':data,
            'contentType':false,
            'processData':false,
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
                xhr.setRequestHeader("Authorization", "JWT "+ token);
            },
            'success':function(response){
                if(typeof callback!='undefined' && response){
                    callback(response)
                }

            },
            error: function(response,status,error){
                if(response.status==401){
                    helperMethods.secureHTTPRequestHandlerImage(url,method,data,callback,'expired')
                }




            }
        })
    },

    ajaxHandlerJWT : function(url,method,data,token,callback){

        var csrf_token = helperMethods.getCookie('csrftoken');

        $.ajax({
            'url':url,
            'type':method,
            'data':JSON.stringify(data),
            'contentType':'application/json',
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
                xhr.setRequestHeader("Authorization", "JWT "+ token);
            },
            'success':function(response,status,xhr){
                if((url.indexOf('wishlist')!=-1 || url.indexOf('cart')!=-1) && (typeof response=="string" && response.indexOf !=undefined && response.indexOf('DOCTYPE')!=-1)){
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
                }else if(typeof callback!='undefined' && response){
                    callback(response)
                }


            },
            error: function(response,status,error){
                if(response.status==401){
                    helperMethods.secureHTTPRequestHandler(url,method,data,callback,'expired')
                }else if((url.indexOf('wishlist')!=-1 || url.indexOf('cart')!=-1) && (typeof response=="string" && response.indexOf !=undefined && response.indexOf('DOCTYPE')!=-1)){
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
                }

            }

      
        })
    },

    getCookie : function(name){
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    },

    secureHTTPRequestHandler : function(url,method,data,callback,type){
        var token = localStorage.getItem('jwt_token')
        if(token=='' || type=='expired'){
            helperMethods.ajaxHandler(base_url+'/accounts/token/','GET',{},function(response){
                localStorage.setItem('token',response.token)
                helperMethods.ajaxHandlerJWT(url,method,data,response.token,callback)
            })
        }
        else{
           helperMethods.ajaxHandlerJWT(url,method,data,token,callback)
        }
    },

    secureHTTPRequestHandlerImage : function(url,method,data,callback,type){
        var token = localStorage.getItem('jwt_token')
        if(token=='' || type=='expired'){
            helperMethods.ajaxHandler(base_url+'/accounts/token/','GET',{},function(response){
                localStorage.setItem('token',response.token)
                helperMethods.ajaxHandlerJWTImage(url,method,data,response.token,callback)
            })
        }
        else{
           helperMethods.ajaxHandlerJWTImage(url,method,data,token,callback)
        }
    },


}





