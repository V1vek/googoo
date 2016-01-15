var review = {
    afterCommentAdded : function(response){
        if(typeof response.id==undefined){
            return;
        }
        var template = _.template($('#comment_added').html())
        $('.recent-comment').append(template(response))
        $('.notice-message').addClass('hide')
        $('.post-form textarea').attr('disabled','disabled')
        $('.post-form textarea').val('')
    }
}

$('.post-form form').on('submit', function(e){
    e.preventDefault()
    var data = {}
    data['book_id'] = $('#book_id').data('id')
    data['review'] = $('.post-form textarea').val()

    var method = 'POST'
    if($('.post-form input[type="submit"]').data('review-id')!=undefined){
        method = 'PUT'
        data['review_id'] = $('.post-form input[type="submit"]').data('review-id')
        data['rating'] = $('.post-form input[type="submit"]').data('rating')
    }

    if(data['review']==''){
        return;
    }
    $('.post-form input[type="submit"]').attr('disabled','disabled')
    ajax_url = base_url+'/api/review/add/'
    helperMethods.secureHTTPRequestHandler(ajax_url, method, data, function(response){
        $('.post-form input[type="submit"]').attr('data-review-id',response.id).attr('data-review',response.review)
        review.afterCommentAdded(response)
    })
})

$('.bookRating input').on('click', function(){
    var data = {}
    data['book_id'] = $('#book_id').data('id')
    data['rating'] = $(this).val()
        console.log($('.post-form input[type="submit"]').data('review-id'))
    var method='POST'
    if($('.post-form input[type="submit"]').data('review-id')!=undefined){
        method = 'PUT'
        data['review_id'] = $('.post-form input[type="submit"]').data('review-id')
        data['review'] = $('.post-form input[type="submit"]').data('review')
    }
    ajax_url = base_url+'/api/review/add/'
    helperMethods.secureHTTPRequestHandler(ajax_url, method, data, function(response){
        $('.post-form input[type="submit"]').attr('data-review-id',response.id).attr('data-rating',response.rating)
    })
})



