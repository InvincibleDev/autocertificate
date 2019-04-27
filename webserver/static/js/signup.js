$("#signup-btn").on('click', function(){
	
	let firstname = $("#firstname").val();
	let lastname = $("#lastname").val();
	let username = $("#username").val();
	let password = $("#password").val();
	let email = $("#email").val();

	var data = {};
	data["first_name"] = firstname;
	data["last_name"] = lastname;
	data["username"] = username;
	data["password"] = password;
	data["email"] = email;
	
	$.ajax({
		method:"POST",
		url:"http://127.0.0.1:8000/api/signup/",
		type: 'application/json',
		data: data,
		success: function(reponse){
			console.log(reponse);
			 window.location.href = "/login/";
		}

	});
});