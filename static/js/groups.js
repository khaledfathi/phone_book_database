//edit group elements
var edit_group_select= document.getElementById("edit_group_select"),
    rename_field =document.getElementById("rename_field"),
    new_group_checkbox = document.getElementById("new_group_checkbox"),
    edit_save_button = document.getElementById("edit_save_button"),
    remove_move_to_new = document.getElementById("remove_move_to_new"),
    new_group_text = document.getElementById("new_group_text"),
//remove elements
    remove_group_select = document.getElementById("remove_group_select"),
    remove_radio = document.getElementsByName("remove_radio"),
    remove_group_move_to = document.getElementById("remove_group_move_to"),
    remove_group_button = document.getElementById("remove_group_button"),
//other
    add_api = document.getElementById("add_api")

//api
var api={
  case:"rename",
  create_new:"0",
  selected_group:"default",
  remove_option:"opt1"
};

/*#*****#* EDIT GROUP*#*****#*/
//checkbox for create new group active text element and disable select element
new_group_checkbox.onclick = function (){
  if (new_group_checkbox.checked){
    api.create_new="1"
    new_group_text.removeAttribute("disabled")
    rename_field.setAttribute("disabled", "")
    edit_group_select.setAttribute("disabled", "")
  }else{
    api.create_new="0"
    new_group_text.setAttribute("disabled", "")
    rename_field.removeAttribute("disabled")
    edit_group_select.removeAttribute("disabled")
  }
};

//add api to form when submit button is clicked
edit_save_button.onclick = function (){
  add_api.value = JSON.stringify(api)
}

//select_group will update summary table
edit_group_select.onchange = function (){
  api["selected_group"] = edit_group_select.options[edit_group_select.selectedIndex].innerText
  api["update_summary"]="1"
  req= new XMLHttpRequest();
  req.onreadystatechange = function (){
    if (this.readyState == 4 && this.status == 200){
      summary = JSON.parse(this.responseText)
      var summary_values = document.getElementsByName("summary_values")
      for (var i=0;i< summary_values.length;i++){
        summary_values[i].innerHTML = summary[i]
      }
    }
  }
  req.open("POST","groups",true)
  req.setRequestHeader("content-type", "application/json")
  req.send(JSON.stringify(api))
}

/*#*****#*END --EDIT GROUP*#*****#*/



/*#*****#* Remove Group *#*****#*/
//actions when radio input selected
for (var i=0;i<remove_radio.length;i++){
  remove_radio[i].addEventListener('click',function(event){
    api.remove_option= event.target.value
    if (event.target.value=="opt2"){
      remove_group_move_to.removeAttribute("disabled")
    }else{
      remove_group_move_to.setAttribute("disabled","")
    }
    if (event.target.value == "opt3"){
      remove_move_to_new.removeAttribute("disabled")
    }else{
      remove_move_to_new.setAttribute("disabled","")
    }
  })
}

//remove gtoup button action
remove_group_button.onclick= function (){
  api.case="remove"
  api.selected_group = remove_group_select.options[remove_group_select.selectedIndex].innerText
  api.selected_group_to = remove_group_move_to.options[remove_group_move_to.selectedIndex].innerText
  add_api.value = JSON.stringify(api)
}
/*#*****#*END --Remove Group *#*****#*/

/*##Change flash message color##*/
var flash_msg = document.getElementById("flash_msg"),
  color_red_messages = [
    "Nothing Changed : Empty Field",
    "Error : You cant Edit 'default' Group",
    "name 'default is not allowed'",
    "Nothing Change : Duplicated Group Name",
    "ERROR : Cant remove default group"
    ],
  color_green_messages =[
    "Group Renamed",
    "Group Removed",
    "Group Removed and contacts moved to other group",
    "New Group Created",
    "Group and contacts are Removed",
    ]

var flash_msg = document.getElementById("flash_msg");



for (var i=0;i<color_red_messages.length;i++){
  if (flash_msg.innerText ==color_red_messages[i]){
    flash_msg.style.color = "red"
    break;
  }
}
for (var i=0;i<color_green_messages.length;i++){
  if (flash_msg.innerText ==color_green_messages[i]){
    flash_msg.style.color = "green"
    break;
  }
}
/*##END -- Change flash message color##*/
