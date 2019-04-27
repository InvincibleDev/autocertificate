var certificates;
$(document).ready(
	function(){

	var maindiv =$("#dashboard");

	$.ajax({
 	method:'GET',
 	url:'http://127.0.0.1:8000/api/certificates/',
 	success:function(response){
    console.log(response);
 		certificates = response;
 		for(let certificate of response){
 			maindiv.append(`

 				
 				<div class="card" style="box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
                      transition: 0.3s;
                      width: 800px; margin:10px;" onmouseover="opacity:0.5;">
  					<a href="/certificate/${parseInt(certificate.id)}">
 					<img src="${certificate.template}" style="width:100%;height:200px;padding:10px;">
 					</a>
 					<div class="container" style="padding: 2px 16px">
 					<h4 style="font-weight:500; letter-spacing:0.1px;font-size:14px;position:relative;top:5px;">${certificate.title}s</h4> 
    				</div>
    			</div>
               
                    			 					
 				`);
 		};
 		console.log(certificates);
 	},
 	beforeSend: function (xhr) {
   			 xhr.setRequestHeader ("Authorization", "Token " + window.localStorage['token']);
	},
 });
	
	
});

$('#certificate-btn').click(function (e) {
    var formdata = new FormData()
    let image = $('#cert').prop('files')[0];
    formdata.append('template', image);
    formdata.append('title', $('#title').val())

    $.ajax({
        method : 'POST',
        enctype: 'multipart/form-data',
        processData: false,
        contentType: false,
        cache: false,
        url : "http://127.0.0.1:8000/api/template/",
        data : formdata,
        beforeSend: function(xhr) {
            xhr.setRequestHeader("Authorization", 'Token ' + window.localStorage["token"])
        },
        success : function(response){
            //callback here on success
            console.log(response);
            // window.location.href = "/dashboard/";
        },
        error : function(e){
            //callback here on error
            console.log('error');
        }
    })
});