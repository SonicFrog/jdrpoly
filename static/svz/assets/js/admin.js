var current_player;

$( document ).ready(function() {
    $.ajaxSetup({
        beforeSend: function(xhr, setting){
            var csrftoken = $("[name=csrfmiddlewaretoken]").val();
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        cache: false
    });

    $("#add-form").submit(function (event) {
        var name = $("#add-form-name").val();
        var sciper = parseInt($("#add-form-sciper").val());
        var email = $("#add-form-email").val();

        if(isNaN(sciper) || name.length == 0) {
            alert("Le nom ne doit pas être vide et le SCIPER doit être un numéro. Ajout annulé.");
        } else {
            create_player(sciper, name, email, function () {
                alert("SCIPER déjà existant. (Ou c'est autre chose, on sait pas)");
            });
        }

        event.preventDefault();
    });

    $( "#search-form" ).submit(function (event) {
        var name = $("#search-form-name").val();
        var sciper = $("#search-form-sciper").val();

        fetch_player(sciper, update_form);

        event.preventDefault();
    });

    $( "#update-form" ).submit(function (event) {
        var p = read_current_player();

        update_player(p.sciper, p.name, p.token_spent, p.zombie, p.contaminations);
        update_form(p);

        event.preventDefault();
    });

    $( "#mail-form" ).submit(function (event) {
        var subject = $("#mail_title").val();
        var body = $("#mail_content").val();
        var zombie = $("#mail_target").val();

        send_mail(subject, body, zombie);

        event.preventDefault();
    });
});


function display_error(message) {
    var err = $("#error-display");
    err.html(message);
    err.show();
}

function display_raw_error(response) {
    display_error(response.detail);
}

function hide_error() {
    $("#error-display").hide();
}

/**
 * Fills the given form with the given player info
 **/
function update_form(player) {
    current_player = player;

    $("#demo-name").val(player.name);
    $("#demo-sciper").val(player.sciper);
    $("#token-spent").html(player.token_spent);
    $("#contaminations").html(player.contaminations);
    $("#zombie-status").prop('checked', player.zombie);
    $("#is-zombie").html(player.zombie?"Oui":"Non");

    reset_input();
}


/**
 * Resets the input field for editing player
 **/
function reset_input() {
    var fields = ["#prefill-spenttoken", "prefill-newcontamination",
                  "#add-form-name", "#add-form-sciper", "#add-form-email",
                  "#mail-title", "#mail-content"];

    for (field of fields) {
        reset_field(field);
    }
}

function reset_form(id) {
    $(id).reset();
}

function reset_field(id) {
    $(id).val("");
}

/**
 * Updates a player (*this function expects the new total for each field*)
 * @param sciper Sciper number for this player
 * @param token The number of token spent
 * @param contaminate a boolean indicating zombie status
 **/
function update_player(sciper, name, token, zombie, contaminations) {
    //URL is hardcoded for now but will be generated using django templates
    var url = "/svz/json/players/" +sciper + "/";

    $.ajax({
        url: url,
        succes: update_form,
        data: {
            "token_spent": token,
            "zombie": zombie,
            "contaminations": contaminations
        },
        error: display_raw_error,
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

function read_current_player() {
    var sciper = $("#demo-sciper").val();
    var name = $("#demo-name").val();
    var tokens = parseInt($("#prefill-spenttoken").val());
    var cont = parseInt($("#prefill-newcontamination").val());
    var zombie = $("#zombie-status").prop('checked');

    if (isNaN(cont))
        cont = 0;
    if (isNaN(tokens))
        tokens = 0;

    var new_cont = parseInt(current_player.contaminations) + cont;
    var new_token = parseInt(current_player.token_spent) + tokens;

    return {
        "sciper": sciper,
        "name": name,
        "zombie": zombie,
        "contaminations": new_cont,
        "token_spent": new_token
    };
}

/**
 * Create a player
 * @param sciper Sciper to create this player
 * @param name Name for this player
 * @param error Callback to be called when creation fails
 **/
function create_player(sciper, name, email, error) {
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
            "name": name,
            "email": email
        }
    });
}

function send_mail(subject, body, zombie) {

    var url = "/svz/json/mail";

    var to;

    switch (zombie) {
    case "True":
        to = true;
        break;
    case "False":
        to = false;
        break;
    case "":
        to = null;
        break;
    default:
        alert("le champ to doit être True ou False.");
    }

    $.ajax(
        url,
        {
            "subject": subject,
            "body": body,
            "zombie" : to
        },
        function () {alert("Message envoyé avec succès!");}
    );
}
