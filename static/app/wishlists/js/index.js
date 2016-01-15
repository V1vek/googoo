function addedToWishlist(response,el){
    if(el.attr('data-to-do')=='move'){
    console.log(el.closest('.check-bookInfo').find('.cBook-remove'))
        el.closest('.check-bookInfo').find('.cBook-remove').trigger('click')
        return;
      }
    if(response.wishlist_id && response.created){

            el.html('<i class="fa fa-heart"></i> Added to <a href="/wishlist/">Wishlist</a>')

    }else if(response.created!=undefined &&!response.created){
        console.log('in')
        $('#wishlist_modal').modal('show')
        var template =_.template($('#wishlist_added').html())
		$('.modal-body').append(template(response.book))
    }
    else if(response.status==302){
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

function removedFromWishlist(response,el){
    console.log( el.closest('.wishlist-item'))
        el.closest('.wishlist-item').remove()

}

$(document).on('click','.add_to_wishlist',function(e){
  e.preventDefault()
  console.log('in')
  var book_id = $(this).attr('data-book-id')
  var el = $(this)
  var ajax_url = base_url+'/api/wishlist/add/'
  helperMethods.secureHTTPRequestHandler(ajax_url, 'POST', {'book_id':book_id}, function(response){
    addedToWishlist(response,el)
  })
})

$('.remove_from_wishlist').on('click',function(e){
    e.preventDefault();
    var book_id = $(this).attr('data-book-id')
    var user_id = $(this).attr('data-user-id')
    var el = $(this)

    var ajax_url = base_url+'/api/wishlist/remove/'
    helperMethods.secureHTTPRequestHandler(ajax_url, 'POST', {'book_id':book_id,'user_id':user_id}, function(response){
       removedFromWishlist(response,el)
    })
    el.closest('.wishlist-item').remove()

    return false;
})

