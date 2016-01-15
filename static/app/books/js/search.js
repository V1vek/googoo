$(document).ready(function(){
	var base_url = 'https://'+window.location.hostname;
	var url = base_url+'/books/search/';
	var next_url = base_url+'/books/search/next/';
	var filter_url = base_url+'/books/search/filter/';
	var search_input = $('.search-bar input');


	var bookSeach = {
		
		searchQueryAsString : function(el){
			var id = $(el).attr('id');
			var id = id.substr(id.lastIndexOf('_')+1)
			var filter_type = $(el).closest('ul.p-search-var-items').attr('filter-type')
			$('#'+filter_type+'_id').val(id)
			return this.buildSearchQuery()
		},

		searchQueryAsArray : function(el){

			el.find('input:checkbox:checked').each(function(){
				var filter=$(this).closest('.p-search-var-items').attr('filter-type')
				var id = $(this).attr('id')
				id = id.substr(id.lastIndexOf('_')+1)
				var value = $('#'+filter+'_id').val()!='' ?$('#'+filter+'_id').val()+','+id : id
				$('#'+filter+'_id').val(value)
			})
			return this.buildSearchQuery()
		},

		buildSearchQuery : function(){
			var self = this;
			var query_url = base_url+'/books/search/';
			$('input.filter_value').each(function(){
				var el = $(this);
				if(el.val()!=''){
					value = $.trim(el.val())
					query_url = self.updateQueryStringParameter(query_url,el.attr('id'),value)
					next_url = self.updateQueryStringParameter(next_url,el.attr('id'),value)
					filter_url = self.updateQueryStringParameter(filter_url,el.attr('id'),value)
				}
			})
			return {'url':query_url,'next_url':next_url,'filter_url':filter_url};
		},
		
		updateQueryStringParameter : function(uri, key, value) {
		  var re = new RegExp("([?&])" + key + "=.*?(&|$)", "i");
		  var separator = uri.indexOf('?') !== -1 ? "&" : "?";
		  if (uri.match(re)) {
		    return uri.replace(re, '$1' + key + "=" + value + '$2');
		  }
		  else {
		    return uri + separator + key + "=" + value;
		  }
		},

		filterText : function (elem) {
	        var value = elem.val().toLowerCase();
	        var filter = elem.attr('data-filter')
	        $(".p-search-var-items[filter-type='"+filter+"'] > li").each(function() {
	            if ($(this).text().toLowerCase().search(value) > -1) {
	                $(this).show();
	            }
	            else {
	                $(this).hide();
	            }
	        });
	    },

		loadBooksOnScroll : function(count){
			var ajax_url = bookSeach.buildSearchQuery()
			if($('#dropdownMenu1').attr('data-filter-applied')!=''){
			    ajax_url = ajax_url['filter_url']
			    data = {'index':count,'type':$('#dropdownMenu1').attr('data-filter-applied')}
			}else{
			    ajax_url = ajax_url['next_url']
			    data = {'index':count}

			}
			this.ajaxHandler(ajax_url,'GET',data,this.renderBookList)
		},
        loadBooksOnSort : function(type){
			var ajax_url = bookSeach.buildSearchQuery()
			ajax_url = ajax_url['filter_url']
			this.ajaxHandler(ajax_url,'GET',{'index':0,'type':type},function(response){
			    $('.p-result').html('')
			    bookSeach.renderBookList(response)
			})
		},
		ajaxHandler : function(url,method,data,callback){
			$.ajax({
				'url':url,
				'type':method,
				'data':data,
				'success':function(response){
					if(response){
						callback(response)
					}
				}
			})
		},

		filterContentByKeyWord: function(key,type){
			var keyword = {}
			keyword[type+'_key']=key
			var ajax_url = base_url+'/'+type+'s/search/';
			this.ajaxHandler(ajax_url,'GET',keyword,function(result){
				bookSeach.renderFilterContent(result,type)
			})
		},

		renderFilterContent: function(results,type){
			$('.'+type+'-results').html('')
			var template =_.template($('#'+type+'_template').html())
			var id = this.getUrlParameter(type+'_id')
			console.log(id, results,id)
			$('.'+type+'-results').append(template({'results':results,'id':id}))
		},

		renderBookList : function(books){
			var template =_.template($('#book_detail').html())
			$('.p-result').append(template({'books':books}))
		},
		
		removeParameter : function(url, parameter){
		  
		  var urlparts= url.split('?');

		  if (urlparts.length>=2)
		  {
		      var urlBase=urlparts.shift(); //get first part, and remove from array
		      var queryString=urlparts.join("?"); //join it back up

		      var prefix = encodeURIComponent(parameter)+'=';
		      var pars = queryString.split(/[&;]/g);
		      for (var i= pars.length; i-->0;)               
		          if (pars[i].lastIndexOf(prefix, 0)!==-1)   //idiom for string.startsWith
		              pars.splice(i, 1);
		      url = urlBase+'?'+pars.join('&');
		  }
		  return url;
		},

		getUrlParameter : function(sParam){
		    var sPageURL = window.location.search.substring(1);
		    var sURLVariables = sPageURL.split('&');
		    for (var i = 0; i < sURLVariables.length; i++) 
		    {
		        var sParameterName = sURLVariables[i].split('=');
		        if (sParameterName[0] == sParam) 
		        {
		            return sParameterName[1];
		        }
		    }
		}     

	};

	// Search within filters by keyword - START

	//Delay function to prevent calling the function on every key press
	var delay = (function(){
	  var timer = 0;
	  return function(callback, ms){
	    clearTimeout (timer);
	    timer = setTimeout(callback, ms);
	  };
	})();

	//On keyup for search within filters
    $('.p-search-cat-box').on('keyup',function(){
    	var self = this
    	delay(function(){
    		var filter = $(self).attr('data-filter');
	    	if(filter=='author' || filter=='publisher'){
	    		$('#'+filter+'_key').val($(self).val())
	    		bookSeach.filterContentByKeyWord($(self).val(),filter)
	    	}else{
	    		bookSeach.filterText($(self))
	    	}
	    }, 600 )
    	
    });

	// Search within filters by keyword - END


    //Filters on change event  - START

    // For category and sub category
	$('.p-search-var-items input:radio').on('change',function(){
		var redirect_url = bookSeach.searchQueryAsString($(this))
		window.location.href = redirect_url['url'];
	})

	// For Authors, Publishers and Binding
	$(document).on('change','.p-search-var-items input:checkbox',function(){
		elem = $(this)
		el = elem.closest('.p-search-var-items')
		$('#'+el.attr('filter-type')+'_id').val('')
		var redirect_url = bookSeach.searchQueryAsArray(elem.closest('.p-search-cat-list'))
		window.location.href = redirect_url['url'];
	})

	//Filters on change event  - END

	// Filters - collapse up and down - START

	$('.filter-container .p-sub-cat i').on('click',function(){
		if($(this).hasClass('fa-minus')){
			$(this).closest('.filter-container').find('.p-search-cat').hide("slide",{direction:'up'},500)
			$(this).removeClass('fa-minus')
			$(this).addClass('fa-plus')
		}else{
			$(this).closest('.filter-container').find('.p-search-cat').show("slide",{direction:'up'},500)
			$(this).removeClass('fa-plus')
			$(this).addClass('fa-minus')
		}
		
	})  

	// Filters - collapse up and down - END


	//Search box Header - START

	$('#search_books').on('click',function(){
		var redirect_url = bookSeach.buildSearchQuery()
		window.location.href = redirect_url['url'];
	})

	$("#query").keyup(function(event){
	    if(event.keyCode == 13){
	        $("#search_books").trigger('click');
	    }
	});

	//Search box Header - END

	//Applied FIlters - remove option 	

	$('.p-filter-title img').on('click',function(){
		var param = $(this).attr('data-applied-filter')
		if(param=='author' || param=='publisher' || param=='binding'){
			var id = $(this).attr('data-filter-id')
			$('#'+param+'_'+id).removeAttr('checked')
			$('#'+param+'_'+id).trigger('change')
		}else{

			redirect_url = bookSeach.removeParameter(window.location.href,param)
			window.location.href = redirect_url
		}
		
	})

	 
	
	//Infinite Scroll - Book Results - START
	if(location.href.indexOf('books/search/')>0){
	    var count =10;
        $(window).scroll(function(){
            if  ($(window).scrollTop() == $(document).height() - $(window).height()){
               bookSeach.loadBooksOnScroll(count);
               count+=10;
            }
        });

	}

	//Infinite Scroll - Book Results - END


	//Filters in Responsive Layout - START

	$('.apply').on('click',function(){
		$('.mobile-filters ul.p-search-var-items span.m_apply_filter').each(function(){
			if($(this).attr('data-is-selected')=='true'){
				var id = $(this).attr('data-id')
				var type = $(this).attr('data-type')
				var value = $('#m_'+type+'_id').val()!=''? $('#m_'+type+'_id').val()+','+id : id
				$('#m_'+type+'_id').val(value)
			}
		})

		$('.m_filter').each(function(){
			var param = $(this).attr('id');
			param = param.substr(param.indexOf('m_')+2)
			value = $.trim($(this).val())
			redirect_url = bookSeach.updateQueryStringParameter(url,param,value)
		})
		window.location.href = redirect_url
	})

	$('.m_apply_filter').on('click',function(){

		if($(this).attr('data-is-selected')=='false'){
			$(this).closest('li').addClass('p-search-var-items-active')
			$(this).attr('data-is-selected','true')
		}else{
			$(this).closest('li').removeClass('p-search-var-items-active')

			$(this).attr('data-is-selected','false')
		}
		
	})

	//Filters in Responsive Layout - END

	$('.back-to-top').on('click', function(){
	    $(window).scrollTop(0   )
	})

	$(window).on('scroll', function(){
	    if($(window).scrollTop()>1200){

	      $('.back-to-top').removeClass('hide')
	    }else{
          $('.back-to-top').addClass('hide')

	    }
	})

	$('.presentation a').on('click', function(e){
	    e.preventDefault();
	    var type= $(this).data('type')
	    bookSeach.loadBooksOnSort(type)
        $('#dropdownMenu1 .sort_filter').text('Sort by :'+type)
        $('#dropdownMenu1').attr('data-filter-applied',type)
	})


    $('#request_books').validate({
        rules : {
            'title': {
                required : true
            },
            'authors': {
                required : true
            },
            'publishers': {
                required : true
            },
        },
        submitHandler: function(form) {
            $('#request_books input[type="submit"]').attr('disabled','disabled')
            var data = {}

            $(form).serializeArray().map(function(x){data[x.name] = x.value;});

            helperMethods.secureHTTPRequestHandler(base_url+'/requested_books/','POST',data,function(response){
                console.log(response)
                if(response.id){
                    $('#request_books .form-group').addClass('hide')
                    $('#request_books').append('<h4>Thanks for sending us the details. We will let you know once we get this book</h4>')
                }
            })
       }

    })

})