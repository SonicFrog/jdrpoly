$( document ).ready(function() {
    $( "#search-form" ).submit(function( event ) {
        var name = $("#search-form-name").val();
        var sciper = $("#search-form-sciper").val();
        $.get("/svz/json/find/"+sciper},
               function (data) {
                   alert("" + data);
               })
            .fail( function () {
                alert("Impossible de trouver le joueur " + 
                      name + " " + sciper + ".");
            });
        event.preventDefault();
    });

    $( "#update-form" ).submit(function( event ) {
        alert("submit update form");
        event.preventDefault();
    });
})
