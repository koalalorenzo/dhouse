var mottos = [
                'live <span style="color: #4e9a06">green</span>',
                'save your <span style="color: #f57900">money</span>',
                'respect the <span style="color: #3465a4">environment</span>',
                'find your <span style="color: #75507b">dream home</span>',
                ];
var current = 0;
function change_motto(){
    $("#mainMotto").fadeOut('slow', function() {
        if(current >= mottos.length){
            current = 0;
        }    
        $("#mainMotto").html(mottos[current]);
        $("#mainMotto").fadeIn('slow', function() {
            setTimeout(change_motto, 1000);
        });
      });
    current += 1;
}