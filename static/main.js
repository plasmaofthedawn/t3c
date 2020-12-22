function newComment() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
           document.getElementById("comment-container").innerHTML = this.responseText;
        }
    };
    xhttp.open("GET", "random_comment", true);
    xhttp.send();
}
function load(location) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
           document.getElementById("content").innerHTML = this.responseText;
        }
    };
    xhttp.open("GET", "get/" + location, true);
    var obj = { Page: location, Url: "/" + location};
    history.pushState(obj, obj.Page, obj.Url);
    xhttp.send();
}
var audioPlaying = false;
function toggleAudio() {
    if(audioPlaying) {
        document.getElementById("background_music").pause();
        audioPlaying = false;
    } else {
        document.getElementById("background_music").play();
        audioPlaying = true;
    }
}