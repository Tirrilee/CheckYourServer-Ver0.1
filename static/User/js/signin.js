$('#SignIn').click(function(e){
    if($(e.target).is('.bg')){
    	$('#SignIn').fadeOut( 500);
    }
})

function Login(){
    $('#SignIn').css("display", "flex").hide().fadeIn( 500 );
}


$('.signup-btn').click(function(){
	$('#SignIn').fadeOut( 500);
	$('#SignUp').css("display", "flex").hide().fadeIn( 500 );
})

$('#SignUp').click(function(e){
    if($(e.target).is('.bg')){
    	$('#SignUp').fadeOut( 500);
    }
})
//
//$('.bg').click(function(e){
//    if($(e.target).is('.bg')){
//    	$('#SignUp').fadeOut( 500);
//    	$('#SignIn').fadeOut( 500);
//    }
//})