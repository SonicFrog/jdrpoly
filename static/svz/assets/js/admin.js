$( document ).ready(function() {
    $( "#search-form" ).submit(function( event ) {
        var name = $("#search-form-name").val();
        var sciper = $("#search-form-sciper").val();

        fetch_player(sciper, update_form);

        event.preventDefault();

        // $.get("/svz/json/find/"+sciper,
        //        function (data) {
        //            alert("" + data.name);
        //        })
        //     .fail( function () {
        //         alert("Impossible de trouver le joueur " +
        //               name + " " + sciper + ".");
        //     });

    });

    $( "#update-form" ).submit(function( event ) {
        alert("submit update form");
        event.preventDefault();
    });
});

/**
 * Fills the given form with the given player info
 **/
function update_form(player) {
    $("#demo-name").val(player.name);
    $("#demo-sciper").val(player.sciper);
    $("#token-spent").html(player.token_spent);
    $("#contaminations").html(player.contaminations);
    $("#zombie-status").prop('checked', player.zombie);
}

/**
 * Updates a player (*this function expects the new total for each field*)
 * @param sciper Sciper number for this player
 * @param token The number of token spent
 * @param contaminate a boolean indicating zombie status
 **/
function update_player(sciper, token, zombie, contaminations) {
    //URL is hardcoded for now but will be generated using django templates
    var url = "/svz/json/players/" +sciper + "/";

    $.ajax({
        url: url,
        data: {
            "token_spent": token,
            "zombie": zombie,
            "contaminations": contaminations
        },
        method: "PATCH"
    });
}

function fetch_player(sciper, callback) {
    var url = "/svz/json/players/" + sciper + "/";

    $.get(url, update_form).fail("Une erreur s'est produite !");
}

/**
 * Finds player by either sciper or name (this can return multiple players)
 * @param sciper Sciper number (partial or complete)
 * @param name Player name (partial or complete)
 * @param callback The function to be called on success with the player's info
 * @param notfound Callback in case player is not found
 * @param error Callback for other error
 **/
function find_player(sciper, name, callback, notfound, error) {
    var url = "/svz/player/find/"+ sciper + "/" + name + "/";

    $.get({
        url: url,
        success: callback,
        error: error,
        statusCode: {
            404: notfound
        }
    });
}

/**
 * Create a player
 * @param sciper Sciper to create this player
 * @param name Name for this player
 * @param error Callback to be called when creation fails
 **/
function create_player(sciper, name, error) {
    //TODO: Fix hardcoded urls
    var url = "/svz/json/players/";

    $.ajax({
        url: url,
        method: "POST",
        error: error,
        statusCode: {
            409: function() {
                alert("Ce sciper existe déjà!");
            }
        },
        data: {
            "sciper": sciper,
            "name": name
        }
    });
}
