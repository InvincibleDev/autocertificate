$(document).ready(function() {
    var location = window.location.href;
    location = location.split("/");
    id = location[location.length - 2];
    $.ajax({
        method: 'GET',
        url: 'http://127.0.0.1:8000/api/certificates/' + id,
        success: function(response) {

            console.log(response)
            var canvas = $("#canvas");
            var img = `<img src='${response[0].template}' style="position:absolute; z-index:1; max-width:100%">`;
            canvas.append(img);

            for (let key of response[0].blanks) {
                let bl = key.blank_no;
                let bs = JSON.parse(key.start);
                let be = JSON.parse(key.end);

                console.log(bs, be);



                console.log("begun.");
                element = document.createElement('div');
                element.innerHTML = bl;
                element.style.position = 'absolute';
                element.style["z-index"] = 100;
                element.className = 'rectangle';
                element.style.width = Math.abs(be[0] - bs[0]) + 'px';
                element.style.height = Math.abs(be[1] - bs[1]) + 'px';
                element.style.left = bs + 'px';
                element.style.top = be + 'px';
                element.style.top = (bs[1] - be[1] < 0) ? bs[1] + 'px' : be[1] + 'px';
                element.style.left = (bs[0] - be[0] < 0) ? bs[0] + 'px' : be[0] + 'px';
                console.log(element);
                canvas.append(element);
                // can=document.getElementById("canvas");
                // console.log(can)
                // can.appendChild(element);
                // can.style.cursor = "crosshair";

                // var blank_no = blank_count;
                // var blank = $("#blank");
                // var input = `<select>`
                // for (let i in h1) {
                //     input += `<option value='${i}'>${ h1[i] }</option>`;

                // }

                // blank.append(input + `</select>`);


                // blank_count++;



            }



        },
        beforeSend: function(xhr) {
            xhr.setRequestHeader("Authorization", "Token " + window.localStorage['token']);
        },
    });
});

var formdata;
$('#file').change(function() {
    //on change event 
    formdata = new FormData();
    if ($(this).prop('files').length > 0) {
        console.log("Got file");
        console.log("a");
        file = $(this).prop('files')[0];
        console.log(file);
        formdata.append("csv", file);

        for (var key of formdata.entries()) {
            console.log(key[0] + ', ' + key[1]);
        }
    }
});

var h1 = [];
$("#upload-csv").on("click", function() {

    console.log("In");
    $.ajax({
        method: 'POST',
        enctype: 'multipart/form-data',
        processData: false,
        contentType: false,
        cache: false,
        url: 'http://127.0.0.1:8000/api/csv/',
        data: formdata,

        beforeSend: function(xhr) {
            xhr.setRequestHeader("Authorization", "Token " + window.localStorage['token']);
        },

        success: function(response) {
            document.getElementById("closebtn").click();
            
            var error = response.detail;
            if (error){
            console.log(error);

            if (response = error) {
                alert(error);
                // alert(error);
                document.getElementById("draw").hidden = true;
            }
                

            }
            

            if (response.headers){

                try{
                     for (var header of response.headers) {
                        console.log(header);
                        h1.push(header);
                    }
            document.getElementById("draw").hidden = false;
                     }
                      catch(err){

        }
                }
       
            console.log(h1);

            
            
            
            
            



        },
    });
});
var blanks = [];

function initDraw(canvas) {
    var mouse = {
        x: 0,
        y: 0,
        startX: 0,
        startY: 0
    }

    var blank_count = 0;

    function setMousePosition(e) {
        var ev = e || window.event; //Moz || IE
        if (ev.pageX) { //Moz
            mouse.x = ev.pageX + window.pageXOffset;
            mouse.y = ev.pageY + window.pageYOffset;
        } else if (ev.clientX) { //IE
            mouse.x = ev.clientX + document.body.scrollLeft;
            mouse.y = ev.clientY + document.body.scrollTop;
        }
    };

    var element = null;
    canvas.onmousemove = function(e) {
        setMousePosition(e);
        if (element !== null) {
            element.style.width = Math.abs(mouse.x - mouse.startX) + 'px';
            element.style.height = Math.abs(mouse.y - mouse.startY) + 'px';
            element.style.left = (mouse.x - mouse.startX < 0) ? mouse.x + 'px' : mouse.startX + 'px';
            element.style.top = (mouse.y - mouse.startY < 0) ? mouse.y + 'px' : mouse.startY + 'px';
        }
    }
    draw.onclick = function(e) {
        var start;
        var end;
        
        var done = false;
        var blank_no;
        canvas.onclick = function(e) {
            var pos = getMousePos(canvas, e);
            var values = Object.values(pos);
            console.log(values);



            // for(let i in values){
            //     console.log(`${values[i]}`);
            // }
            if (element !== null) {

                var pos = getMousePos(canvas, e);
                console.log(pos);
                var values = Object.values(pos);
                console.log(values);
                end = values;

                element = null;
                canvas.style.cursor = "default";
                console.log("finished");
                // for(let key of canvas.onclick){

                console.log(blank_count);
                var blank_no = blank_count;
                var blank_no1=$("#blank_no");

                blank_no1.append("<br><br />"+"Blank Number"+blank_no);
                console.log(blank_no1);


                // };
                var blank = $("#blank");
                var input = `<select  class="custom-select">`
                for (let i in h1) {
                    input += `<option value='${i}'>${ h1[i] }</option>`;

                }

                blank.append("<br><br />"+input + `</select>`);



                blank_count++;


                done = true;
                // input.style["width"] = "300px";

                document.getElementById("submit-btn").hidden = false;
                document.getElementById("download").hidden = false;
                var size=document.getElementById("input");
                size.style["width"]="300px";

            } else {

                var pos = getMousePos(canvas, e);
                console.log(pos);
                var values = Object.values(pos);
                console.log(values);
                start = values;


                console.log("begun.");
                mouse.startX = mouse.x;
                mouse.startY = mouse.y;
                element = document.createElement('div');
                element.innerHTML = "";
                element.className = 'rectangle';
                element.style.left = mouse.x + 'px';
                element.style.top = mouse.y + 'px';
                console.log(element);
                canvas.appendChild(element);
                canvas.style.cursor = "crosshair";
            }



            var location = window.location.href;
            location = location.split("/");
            var id = location[location.length - 2];

            if (done) {

                var blank = {
                    start: start,
                    end: end,
                    blank_no: blank_no
                };


                console.log(blank);
                blanks.push(blank);
                console.log(blanks);
                done = false;

            }
        }

    }



    function getMousePos(canvas, evt) {
        var rect = canvas.getBoundingClientRect();

        return {
            x: evt.clientX - rect.left,
            y: evt.clientY - rect.top,

        };
    }
}


$(document).on('click',"#submit-btn", function() {
    initDraw();
    
    var data = {};
    data["template_id"] = id;
    data["blanks"] = blanks;


    $.ajax({
        method: 'POST',
        url: 'http://127.0.0.1:8000/api/blankupload/',
        data: JSON.stringify(data),
        dataType: 'application/json',
        beforeSend: function(xhr) {
            xhr.setRequestHeader("Authorization", "Token " + window.localStorage['token']);
        },
        success: function(response) {
            console.log(response);

        }
    });
});