function reSendotp(username, id) {
	text = document.getElementById(id);
	text.innerText = "Sending...";
	$.ajax({
		type: 'GET',
		url: '/resend-otp',
		data: {user:username},
		success: function(data){
			text.innerText = data;
       }
	})
}