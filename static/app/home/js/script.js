$(document).ready(function(){
	
	var appHome = {
		searchBooks : function(){
			var query = $('.mega-search-box').val();
			var query = query!='' ? "?query="+query: '';
			window.location.href="/books/search/"+query;
		}
	};

	$('.btn-mega-search').on('click',function(){
		appHome.searchBooks();
	})

	$(".mega-search-box").keyup(function(event){
	    if(event.keyCode == 13){
	        $(".btn-mega-search").click();
	    }
	});

	function setHeight() {
		var windowHeight = $(window).innerHeight() ;  
		$('#banner').css('min-height',windowHeight );
	};
	
	setHeight();

	if(location.search.indexOf('email_verified')!=-1){
	     $('.authentication[data-type="signin"]').trigger('click');
	     $('.error_display').text("Email verified successfully.")
	}


})