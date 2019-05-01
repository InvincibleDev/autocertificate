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

 				
 				<div class="my" style="box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
                      transition: 0.3s;
                      width:500px;height:340px; margin:50px;">

  					<a href="/certificate/${parseInt(certificate.id)}">
 					<img src="${certificate.template}" style="width:100%;height:300px;padding:10px;">
                    <h4 style="font-weight:500; letter-spacing:0.1px;font-size:25px;position:relative;top:2px;text-align:center;color:#079992;"><b>${certificate.title}</b></h4> 
 					</a>
 					
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
            var error1=response.detail;
            alert(error1);
            window.location.href = "/dashboard/";
        },
        error : function(e){
            //callback here on error
            console.log('error');
        }
    })
});