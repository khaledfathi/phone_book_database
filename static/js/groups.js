//edit group elements
var edit_group_select= document.getElementById("edit_group_select"),
    rename_field =document.getElementById("rename_field"),
    new_group_checkbox = document.getElementById("new_group_checkbox"),
    edit_save_button = document.getElementById("edit_save_button"),
    remove_move_to_new = document.getElementById("remove_move_to_new"),
//remove elements
    remove_group_select = document.getElementById("remove_group_select"),
    remove_radio = document.getElementsByName("remove_radio"),
    remove_group_move_to = document.getElementById("remove_group_move_to"),
    remove_move_to_text = document.getElementById("remove_move_to_text"),
    new_group_text = document.getElementById("new_group_text"),
//other
    add_api = document.getElementById("add_api")


//api
var api={
  case:"rename",
  selected_group:"default",

};

/*#*****#* EDIT GROUP*#*****#*/
//checkbox for create new group active text element and disable select element
new_group_checkbox.onclick = function (){
  if (new_group_checkbox.checked){
    api.case="create_new"
    new_group_text.removeAttribute("disabled")
    rename_field.setAttribute("disabled", "")
    edit_group_select.setAttribute("disabled", "")
  }else{
    api.case="rename"
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
  api["case"]="update_summary"
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








/*#*****#* Summary*#*****#*/

/*#*****#*END --Summary*#*****#*/

/*#*****#* Remove Group *#*****#*/

//actions when radio input selected
for (var i=0;i<remove_radio.length;i++){
  remove_radio[i].addEventListener('click',function(event){
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

/*#*****#*END --Remove Group *#*****#*/




/*****/
setInterval(function(){console.log(JSON.stringify(api) , add_api.value)} , 500)
