window.onkeydown = function(e) {
    if(e.keyCode == 32 && e.target == document.body) {
        e.preventDefault();
        return false;
    }
};

$(document).ready(function()
    {
        console.log("new loop");
        var source = new EventSource("/progress");
        source.onmessage = function(event)
            {
                document.getElementsByClassName("text")[0].innerHTML = event.data;
                if (event.data.includes("<br>")) {
                    event.target.close();
                    document.getElementsByClassName("title")[0].innerHTML = "Done!";
                    var a = document.createElement('a');
                    var img = document.createElement("img");
                    img.height = "60";
                    img.src = "../static/images/ok_button.png";
                    a.setAttribute('href', "/about");
                    a.appendChild(img);
                    var prt = document.getElementById('return');
                    prt.appendChild(a);

                }
            }, false
        
    }
);