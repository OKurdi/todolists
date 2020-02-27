function confirm_delete_list(){
    return confirm('Are you sure you want to delete this list?')
}

function confirm_delete_entry(){
    return confirm('Are you sure you want to delete this task?')
}

function enable_buttons(){
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

function mark_entry_done(entry_id) {
    $.ajax({
          url: '/polls/ajax/entrystatus/',
          type: 'POST',
          data: {'entry_id': entry_id},
          dataType:'json',
          success: function(data){
              console.log("requested access complete");
          }
    })
}

function check(entry_check_box, entry){
    if(entry.selected == "checked"){
            document.getElementById(entry_check_box.id).checked = true;
    }else{
            document.getElementById(entry_check_box.id).checked = false;
    }
}

$(function() {
    // This function gets cookie with a given name
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

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
});