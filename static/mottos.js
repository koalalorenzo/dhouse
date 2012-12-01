var mottos = [""];
var current = 0;

function change_motto(){
    current += 1;
    $("#mainMotto").fadeOut('slow', function() {
        $("#mainMotto").html("Figata"+current);
        $("#mainMotto").fadeIn('slow', function() {
            setTimeout(change_motto, 1000);
        });
      });
    console.log("Pronto");
}