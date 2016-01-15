
var addBooks = {

    renderSubCategory : function(response){
        if(typeof response.sub_categories!='undefined'){
            var sub_categories = response.sub_categories;
            $('#sub_category').html('')

            for (var i in response.sub_categories){
                var option = '<option value="'+sub_categories[i].id+'">'+sub_categories[i].name+'<option>';
                $('#sub_category').append(option);
            }

            $('#sub_category').append('<option value="others">Others</option>');

        }
    },
    afterAddedBooks : function(response){
        if(response.status=='success'){
            $('add_books input').each(function(){
                $(this).val('')
            })
        }
        window.location.href='/sellers/dashboard/'
    },
    renderBookDetails: function(response){
        if(response.book =='undefined' || response.error=='undefined'){
            return;
        }

        $('#add_books input.book_fields').each(function(){
            var el = $(this);
            if(response.book[el.attr('name')]!='undefined'){
                el.val(response.book[el.attr('name')])
            }
            if(response.book.hasOwnProperty('image_url')){
                el.attr('disabled','disabled')
            }

        })

        if(response.book.image_url){
            $('#book_image_container').attr('src',response.book.image_url)
            $('.upload_book_pic').addClass('hide')
        }

        if(response.book['category_id']!=undefined){
            $('#category').val(response.book['category_id'])
            $("#category").prop("disabled", true);
        }

        $('#category').trigger('change')

    },

    afterBulkUpload : function(response){

    },
    afterBookImageUpload : function(response){
        if(response.image_url){
            $('#add_books input[name="image_url"]').val(response.image_url)
            $('#book_image_container').attr('src',response.image_url)
        }
    }
}
$('.btn-books').on('click',function(){
        $('.add-books-form').removeClass('hide')
        $('.add-books-form').show('slide',{direction:'up'},600)
        $('.add-books').addClass('hide')
        $('.details,.order-details').addClass('hide')
})

$('.back-add-books').on('click',function(){
        var open_modal = false;
        $('.add-books-form input').each(function(){
            if($(this).val()!=''){
                open_modal = true;
            }
        })

        if(open_modal){
            $('#backToInventory').modal('show')
        }else{
            $('.add-books-form').hide('slide',{direction:'up'},600)
            $('.add-books').removeClass('hide')
            $('.details,.order-details').removeClass('hide')
        }


})

$(document).on('click','.go-back-inventory', function(){
    $('.add-books-form input').each(function(){
        $(this).val('')
    })
    $('.add-books-form').hide('slide',{direction:'up'},600)
    $('.add-books').removeClass('hide')
    $('.details,.order-details').removeClass('hide')
})

$('#add_books #category').on('change',function(){
    var category_id = $(this).val()

    if(category_id!=''){
        var ajax_url = base_url+'/api/category/'+category_id
        helperMethods.secureHTTPRequestHandler(ajax_url, 'GET', {},addBooks.renderSubCategory)
    }else{
        $('#sub_category').html('')
        $('#sub_category').append('<option value="">Choose Subcategory</option>');
    }
})

$('#book_condition').on('change',function(){
    var book_condition = $(this).val()

    if(book_condition=='1'){
        $('.new_quantity').removeClass('hide')
        $('.old_quantity').addClass('hide')

    }else if(book_condition=='2'){
        $('.new_quantity').addClass('hide')
        $('.old_quantity').removeClass('hide')
    }else if(book_condition=='3'){
        $('.new_quantity').removeClass('hide')
        $('.old_quantity').removeClass('hide')
    }
})

var delay = (function(){
  var timer = 0;
  return function(callback, ms){
    clearTimeout (timer);
    timer = setTimeout(callback, ms);
  };
})();



$.validator.addMethod("newBookQuantityRequired", function(value, element) {
        if($('#book_condition').val() == '1' ||  $('#book_condition').val() == '3'){
            return $(element).val()=='' ? false : true;
        }
}, "quantity cannot be empty");

$.validator.addMethod("oldBookQuantityRequired", function(value, element) {
        if($('#book_condition').val() == '2' ||  $('#book_condition').val() == '3'){
            console.log( $('#good_condition').val()=='' && $('#average_condition').val()=='' && $('#acceptable_condition').val()=='')
            return $('#good_condition').val()=='' && $('#average_condition').val()=='' && $('#acceptable_condition').val()=='' ? false : true;
        }

}, "Quantity required for any of the book condition");

$('#add_books').validate({
   rules: {
        "title": {
            required: true,
        },
        "isbn_13": {
            required: true,
            number:true
        },
        "isbn_10": {
            number:true
        },
        "authors": {
            required: true,
        },
        "publishers": {
            required: true,
        },

        "pages": {
            required: true,
        },
        "binding": {
            required: true,
        },
        "selling_price": {
            required: true,
            number: true,
        },
        "price": {
            required: true,
            number: true,
        },
        "category_id": {
            required: true,
        },
        "sub_category_id": {
            required: true,
        },
        "book_condition": {
            required: true,
        },
        "book_quantity": {
            number: true,
            required: true,
        },
        "book_condition": {
            number: true,
            required: true,
        },
        "edition_and_year": {
            required: true,
        }
   },
   submitHandler: function(form) {
        var data = {}

        $(form).find('.book_fields').each(function(){
             data[$(this).attr('name')] = $(this).val();
        })


        data['book_conditions']=[]
        $(form).find('.bookMulti .bm-addSection').each(function(i){
            var self = this;

            if ($(self).find('select[name="book_condition"]').val()!='' && $(self).find('input[name="book_quantity"]').val()!=''
                                                  && $(self).find('input[name="selling_price"]').val()!=''){


                data['book_conditions'].push({
                    'book_condition' : $(self).find('select[name="book_condition"]').val(),
                    'book_quantity' : $(self).find('input[name="book_quantity"]').val(),
                    'selling_price': $(self).find('input[name="selling_price"]').val()
                });

            }
        })

        var ajax_url = base_url+'/api/sellers/books/'
        helperMethods.secureHTTPRequestHandler(ajax_url, 'POST', data,addBooks.afterAddedBooks)

   }

});



//On keyup for search within filters
$('#isbn_10,#isbn_13').on('keyup',function(){
    var self = this
    var keyword = $.trim($(this).val())

    delay(function(){
        var url = base_url+'/api/books/search/?keyword='+keyword;
        if (keyword!=''){
             helperMethods.secureHTTPRequestHandler(url,'GET',{},addBooks.renderBookDetails)
        }
    }, 1000 )

});


// Add books - bulk upload
$('.btn-mulUpld').on('click',function(){
    $('.upload-books-excel').trigger('click');
})

$('.upload-books-excel').on('change',function(){
    var url = base_url+'/api/sellers/upload_books/'
    var file = document.querySelector('.upload-books-excel').files[0]
    var file_name = file.name
    var ext = file_name.substr(file_name.lastIndexOf('.')+1)
    var fd = new FormData();
    fd.append("file_url", file);
    fd.append("ext", ext);

    helperMethods.secureHTTPRequestHandlerImage(url,'POST',fd,addBooks.afterBulkUpload)
})

// Add books - book image
$('.upload_book_pic').on('click',function(e){
    e.preventDefault();
    $('#book_image').trigger('click');
})

$('#book_image').on('change',function(){
    var url = base_url+'/api/sellers/upload_book_image/'
    var file = document.querySelector('#book_image').files[0]
    var file_name = file.name
    var ext = file_name.substr(file_name.lastIndexOf('.')+1)
    var fd = new FormData();
    fd.append("book_image", file);
    fd.append("ext", ext);

    if($('#add_books #isbn_10').val()!=''){
        fd.append("isbn", $('#add_books #isbn_10').val());
        $('#book_image-error').addClass('hide')
    }else if($('#add_books #isbn_13').val()!=''){
        $('#book_image-error').addClass('hide')
        fd.append("isbn", $('#add_books #isbn_10').val());
    }else if($('#add_books #book_title').val()!=''){
        $('#book_image-error').addClass('hide')
        var title = $('#add_books #book_title').val().split(" ").join('_')
        fd.append("isbn", title);
    }else{
        $('#book_image-error').removeClass('hide')
        return;
    }

    helperMethods.secureHTTPRequestHandlerImage(url,'POST',fd,addBooks.afterBookImageUpload)
})

$(document).on('click','.add_book_condition', function(){
    var is_empty = false;
    $('.bookMulti .bm-addSection select').css('border','none')
    $('.bookMulti .bm-addSection select').each(function(){
        var value = $(this).val();
        if(value==''){
            is_empty=true;
            $(this).css('border','1px solid red')
        }
    })

    if(is_empty){
        return;
    }

    $(this).closest('.bm-button').addClass('hide')
    var bk_condition_template = _.template($('#book_condition_tmpl').html());
    id = $('.bookMulti .bm-addSection').length+1;
    $('.bookMulti').append(bk_condition_template({'id':id}))

    $('.bookMulti .bm-addSection select').each(function(){
        var value = $(this).val();
        if(value!=''){
            $('.bookMulti .bm-addSection select:last option[value="'+value+'"]').remove()

        }
    })

    if($('.bookMulti .bm-addSection select:last option').length<3){
        $('.add_book_condition').closest('.bm-button').addClass('hide')
    }

 })

 $(document).on('click','.bm-minus', function(){

    $(this).closest('.bm-addSection').remove()
    $('.add_book_condition:last').closest('.bm-button').removeClass('hide')

 })

 if(location.href.indexOf('edit')!=-1){

    $('#isbn_13').trigger('keyup')
 }

// $(document).on('click','.tedit-desktop', function(e){
//    e.preventDefault();
//    var $tbl_row = $(this).closest('tr');
//    $tbl_row.find('td.editable .display_text').addClass('hide')
//    $tbl_row.find('td.editable .input_value').removeClass('hide')
//    $tbl_row.find('.display_mode').addClass('hide')
//    $tbl_row.find('.edit_mode').removeClass('hide')
// })

