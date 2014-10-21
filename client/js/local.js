//PAGINATION

function pagination(){
    //how much items per page to show  
    var show_per_page = 5;  
    //getting the amount of elements inside content div  
    var number_of_items = $('#gasbody').children().size(); 
    //calculate the number of pages we are going to have  
    var number_of_pages = Math.ceil(number_of_items/show_per_page);  
  
    //set the value of our hidden input fields  
    $('#current_page').val(0);  
    $('#show_per_page').val(show_per_page);  
  
    var navigation_html = '<ul class="pagination"><li><a href="javascript:previous();">&laquo;</a></li>';  
    var current_link = 0;  
    while(number_of_pages > current_link){  
        navigation_html += '<li><a href="javascript:go_to_page(' + current_link +')" longdesc="' + current_link +'">'+ (current_link + 1) +'</a></li>';  
        current_link++;  
    }  
    navigation_html += '<li><a href="javascript:next();">Next</a></li></ul>';  
  
    $('#page_navigation').html(navigation_html);  
  
    //add active_page class to the first page link  
    $('#page_navigation .page_link:first').addClass('active_page');  
  
    //hide all the elements inside content div  
    $('#gasbody').children().css('display', 'none');  
  
    //and show the first n (show_per_page) elements  
    //$('#gasbody').children().slice(0, show_per_page).css('display', 'inline'); 
    $('#gasbody').children().slice(0, show_per_page).css('display', ''); 
}


function previous(){  
  
    new_page = parseInt($('#current_page').val()) - 1; 
    alert('Destinazione ' + new_page + ' Pagina corrente ' + $('#current_page').val());
    //if there is an item before the current active link run the function  
    if($('.active_page').prev('.page_link').length==true){  
        go_to_page(new_page);
    }  
  
}  
  
function next(){  
    new_page = parseInt($('#current_page').val()) + 1;  
    alert('Destinazione ' + new_page + ' Pagina corrente ' + $('#current_page').val());
    //if there is an item after the current active link run the function  
    if($('.active_page').next('.page_link').length==true){  
        go_to_page(new_page);  
    }  
  
}  
function go_to_page(page_num){  
    //get the number of items shown per page  
    var show_per_page = parseInt($('#show_per_page').val());  
  
    //get the element number where to start the slice from  
    start_from = page_num * show_per_page;  
  
    //get the element number where to end the slice  
    end_on = start_from + show_per_page;  
  
    //hide all children elements of content div, get specific items and show them  
    //$('#gasbody').children().css('display', 'none').slice(start_from, end_on).css('display', 'block');  
  	$('#gasbody').children().css('display', 'none').slice(start_from, end_on).css('display', '');  

    /*get the page link that has longdesc attribute of the current page and add active_page class to it 
    and remove that class from previously active page link*/  
    $('.page_link[longdesc=' + page_num +']').addClass('active_page').siblings('.active_page').removeClass('active_page');  
  
    //update the current page input field  
    $('#current_page').val(page_num);  
}  

//SEARCH bar

$('#search-bar').keyup(function(){
	//split the current value of searchInput
    var data = this.value.split(" ");
    //create a jquery object of the rows
    var jo = $("#gasbody").find("tr");
    if (this.value == "") {
        jo.show();
        return;
    }
    //hide all the rows
    jo.hide();

    //Recusively filter the jquery object to get results.
    jo.filter(function (i, v) {
        var $t = $(this);
        for (var d = 0; d < data.length; ++d) {

            if ($t.is(":contains('" + data[d] + "')")) {
                return true;
            }  
            //$("#gasbody").replaceWith("<td colspan=\"7\" class=\"nofound\">Nothing found</td>");
        }
        //$("#gasbody").replaceWith("<td colspan=\"7\" class=\"nofound\">Nothing found</td>");
        return false;
    })
    //show the rows that match.
    .show();
	}).focus(function () {
	    this.value = "";
	    $(this).css({
	        "color": "black"
	    });
	    $(this).unbind('focus');
	}).css({
	    "color": "#C0C0C0"
});


function smartpaginator(){

	var number_of_items = $('#gasbody').children().size(); 
	$('#page_navigation').smartpaginator({ totalrecords: number_of_items, 
                                     	recordsperpage: 2, 
                                     	length:3,
                                      	datacontainer: 'gasbody', 
                                      	dataelement: 'tr',
                                      	controlsalways:true,
                                      	theme: 'green'
                                       });
}

//-------------------------//
/* DOCUMENT READY FUNCTION */
//-------------------------//

$(document).ready(function(){
	//pagination();
	//smartpaginator();
	/*Modernizr.addTest('overflowscrolling', function(){
	  return Modernizr.testAllProps("overflowScrolling");
	});*/


	//$(".order").tablesorter(); 
	//$(".gas").tablesorter(); 

   /*resizing();
   $( window ).resize(function() {
   		resizing();
	});*/
		
});

//RESIZING FUNCTION - do not delete!

/*function resizing(){

	if ($(window).width() > 991){
			height = $(window).height();
			var el = $('.slide');
			var elpos_original = el.offset().top;
			$(window).scroll(function(){
				if ($(window).width() > 991){
				    var elpos = el.offset().top;
				    var windowpos = $(window).scrollTop();
				    var finaldestination = windowpos;
				    //alert(windowpos);
				    if(windowpos<elpos_original) {
				        finaldestination = elpos_original;
				        el.stop().css({'margin-top':height/2});
				    } else {
				        el.stop().animate({'margin-top':finaldestination-elpos_original+(height/2)},500);
				    }
				}
			});
	}else{
		$('.slide').css({'margin-top':0});
	}
}*/

//HIDING-SHOWING BLOCKS!!!//

	clicked = true;
	$("#hideblock").click(function(){
		if (clicked === true)
		{
			$(".first_block").addClass("first_block_max");
			$("#hideblock i").removeClass("fa-chevron-right");
			$("#hideblock i").addClass("fa-chevron-left");
			clicked = false;
		}else{
			clicked = true;
			$(".first_block").removeClass("first_block_max");
			$("#hideblock i").removeClass("fa-chevron-left");
		    $("#hideblock i").addClass("fa-chevron-right");
		}			
	});




