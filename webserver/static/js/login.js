$("#login-btn").on('click', function(){
	let username = $("#username").val();
	let password = $("#password").val();

	var data = {};
	data["username"] = username;
	data["password"] = password;
	
	$.ajax({
		method:"POST",
		url:"http://127.0.0.1:8000/api/api-token-auth/",
		type: 'application/json',
		data: data,
		success: function(reponse){
			console.log(reponse);
			 window.localStorage['token']=reponse['token'];
			 window.location.href = "/dashboard/";
		}

	});
});