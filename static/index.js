$("#main_right").css({"position":"relative","opacity": 0, "left":"+=100"});
$("#main_right").animate({left:0, opacity:1},2000);

$("#main_left").css({"position":"relative","opacity": 0, "right":"+=100"});
$("#main_left").animate({right:0, opacity:1},2000);

$("#header_mid").css({"position":"relative","opacity": 0, "left":"+=100"});
$("#header_mid").animate({left:0, opacity:1},2000);

$("#header_dot").css({"position":"relative","opacity": 0, "center":"+=100"});
$("#header_dot").animate({center:0, opacity:1},2000);

$("#header_point").css({"position":"relative","opacity": 0, "right":"+=100"});
$("#header_point").animate({right:0, opacity:1},2000);


var latBox = document.getElementById("latBox");
var lonBox = document.getElementById("lonBox");

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        latBox.innerHTML = "Geolocation is not supported by this browser.";
    }
}

function showPosition(position) {
    latBox.value = position.coords.latitude;
    lonBox.value = position.coords.longitude;
}
