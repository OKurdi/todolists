
function confirm_delete(){
    return confirm('Are you sure you want to delete this?')
}
/*
function activate-buttons(){
    var list_id= document.getElementByName("list_id").value
    if (list_id == null){
        document.getElementByName("view_tasks").disable=true
        document.getElementByName("rename_list").disable=true
        document.getElementByName("add_list").disable=true
        document.getElementByName("delete_list").disable=true
    }else{
        document.getElementByName("view_tasks").disable=false
        document.getElementByName("rename_list").disable=false
        document.getElementByName("add_list").disable=false
        document.getElementByName("delete_list").disable=false
    }
}
*/
function activate_buttons(){
    document.getElementById("view_tasks").disabled =false
    document.getElementById("rename_list").disabled =false
    document.getElementById("add_member").disabled =false
    document.getElementById("delete_list").disabled =false
}


function activate_entries_buttons(){
    document.getElementById("delete_task").disabled = false
}

/*
function mark_entry_done(){
    if(document.getElementByName("checkboxdone").checked== true){
        entry_id = document.getElementByName("entry").value

    }

}
*/

function mark_entry_done(entry_check_box) {

    if(entry_check_box.checked == true){
          entry_id = entry_check_box.value
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
    }

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
$("#id_nick_name").focusout(function (e) {
        e.preventDefault();
        // get the nickname
        var nick_name = $(this).val();
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