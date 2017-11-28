window.onkeydown = function(e) {
    if(e.keyCode == 32 && e.target == document.body) {
        e.preventDefault();
        return false;
    }
};

$(document).ready(function()
    {
        var source = new EventSource("/progress");
        var string;
        source.onmessage = function(event)
            {
                console.log(event.data);
                document.getElementsByClassName("text")[0].innerHTML = event.data;
                if (event.data.includes("<br>")) {
                    event.target.close();
                    document.getElementsByClassName("title")[0].innerHTML = "Done!";

                    var stars = document.getElementsByClassName("title")[0];
                    $(stars).celebrate({
                          particles: 25,
                          radius: 2000,
                          color: "#e7c358",
                          unicode: '\u2605', // star
                          start_size: '20',
                          min_end_size: '5',
                          max_end_size: '10',
                          max_duration: 3000,
                          min_duration: 2000,
                        });

                    var img2 = document.createElement("img");
                    img2.height = "70";
                    img2.src = "../static/images/text_button.png";
                    var b = document.createElement('a');
                    b.setAttribute('href', "#");
                    b.onclick = function(){
                        alert(string);
                    }
                    b.appendChild(img2);

                    var a = document.createElement('a');
                    var img1 = document.createElement("img");
                    img1.height = "70";
                    img1.src = "../static/images/ok_button.png";
                    a.setAttribute('href', "/about");
                    a.appendChild(img1);
                    var prt = document.getElementById('return');
                    prt.appendChild(b);
                    prt.appendChild(a);

                    $(img1).hover(function(){
                        $(this).addClass('shadow');;
                    }, function(){
                        $(this).removeClass('shadow');
                    });

                    $(img2).hover(function(){
                        $(this).addClass('shadow');;
                    }, function(){
                        $(this).removeClass('shadow');
                    });

                }
                else {
                    string += event.data + "\n";
                }
            }, false


        
    }
);
