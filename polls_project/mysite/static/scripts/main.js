

function confirm_delete_list(){
    return confirm('Are you sure you want to delete this list?')
}
function confirm_delete_entry(){
    return confirm('Are you sure you want to delete this task?')
}

function activate_buttons(){
    document.getElementById("view_tasks").disabled =false
    document.getElementById("rename_list").disabled =false
    document.getElementById("add_member").disabled =false
    document.getElementById("delete_list").disabled =false
}
function activate_view_tasks_button(){
    document.getElementById("view_tasks").disabled =false
}

function activate_entries_buttons(){
    document.getElementById("delete_task").disabled = false
}


 $('.entrycheckbox').onchange(function(){
    var catid;
    catid = $(this).attr("data-catid");
    var csrftoken = Cookies.get('csrftoken');
    $.ajax({
          headers: {'X-CSRFToken': csrftoken},
          type: 'POST',
          url: "{% url 'polls:entrystatus' %}",
          data: {"entry_id": entry_id},
          dataType:'json',
          success: function(json){
              console.log("requested access complete");
          }
    })
});

function mark_entry_done(entry_id) {
   //return confirm("confirmation message from mark_entry_done with entry_id =" + entry_id );


    var csrftoken = Cookies.get('csrftoken');
    $.ajax({
          headers: {'X-CSRFToken': csrftoken},
          type: 'POST',
          url: "{% url 'polls:entrystatus' %}",
          data: {"entry_id": entry_id},
          dataType:'json',
          success: function(json){
              console.log("requested access complete");
          }
    })

    //var csrftoken = Cookies.get('csrftoken');
/*
    var request = new Request(
        url: '{% url 'polls:entrystatus'%}',//"ajax/entrystatus",
        {headers: {'X-CSRFToken': csrftoken}}
    );
    fetch(request, {
        method: 'POST',
        mode: 'same-origin'  // Do not send CSRF token to another domain.
    }).then(function(response) {
        // ...
    });
  */  /*
    var request = $.ajax({
          type: 'POST',
          url: "ajax/entrystatus",
          data: {"entry_id": entry_id},
          dataType:'json',
          contentType: "application/json",
          data: JSON.stringify(requestData),
          success: function(json){
              console.log("requested access complete");
          }
    })
    request.done()
    */
    /*
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
              document.getElementById("demo").innerHTML = this.responseText;
        }
    };
    xhttp.open("GET", {% url 'polls:entries'%}, true);
    xhttp.send();
    */
}


/*
$("#entry1").check(function (e) {
        //e.preventDefault();
        // get the nickname
        //var nick_name = $(this).val();
        // GET AJAX request
        $.ajax({
            type: 'PUT',
            url: "{% url 'polls:entries' %}",
            data: {"entry_id": entry_id},
            success: function (response) {
                // if not valid user, alert the user
                if(!response["valid"]){
                    alert("You cannot create a friend with same nick name");
                    var nickName = $("#id_nick_name");
                    nickName.val("")
                    nickName.focus()
                }
            },
            error: function (response) {
                console.log(response)
            }
        })
    })

*/



function check(entry_check_box, entry){
    return confirm('Are you sure you want to delete this?', entry.id);
    if(entry.selected == "checked"){
            document.getElementById(entry_check_box.id).checked = true;
    }else{
            document.getElementById(entry_check_box.id).checked = false;
    }
}


// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

