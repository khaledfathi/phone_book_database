//varibale for HTML ELEMENT
var table_div =document.getElementById("table_div"),

name_ = document.getElementById("name_"),
nickname = document.getElementById("nickname"),
phone_number= document.getElementById("phone_number"),
address = document.getElementById("address"),
work = document.getElementById("work"),
email = document.getElementById("email"),
notes = document.getElementById("notes"),
group_checkbox = document.getElementById("group_checkbox"),
group_list = document.getElementById("group_list"),
group_text = document.getElementById("group_text"),
groups_rules = document.getElementById("groups_rules"),
new_group_flag =document.getElementById("new_group_flag"),

cancle_button = document.getElementById("cancle_button"),
edit_section =document.getElementById("edit_section"),
filter = document.getElementById("filter"),
filter_by = document.getElementsByName("filter_by"),
res_table = document.getElementById("res_table"),
update_button = document.getElementById("update_button"),
id_value = document.getElementById("id_value"),
flash_message = document.getElementById("flash_message");


//api structure
var api={
  case:"",
  filter:"",
  filter_by:"",
  selected:"",
  id:"",
  name : "",
  nickname:"",
  phone_number:"",
  address:"",
  work:"",
  email:"",
  notes:"",
  group:"",
  new_group:"",
  group_list:"",
  group_rules:"",
  html:""
};

/*##GENERAL FUNCTIONS ##*/

/*##END -- GENERAL FUNCTIONS ##*/

/*### all table tr onclick event , with ajax - return query result###*/
var tr = document.getElementsByTagName("tr");
for (var i=0;i<tr.length;i++){
  tr[i].addEventListener('click', select_for_edit, false)
}

function select_for_edit (event){
  try{ // i used 'try' because this element is not be created yet
      flash_message.innerHTML="" //remove last flash message
  }catch{}

  id_value.value = event.target.id //set query id to send with form
  api.id = event.target.id
  api.case="edit"
  var req = new XMLHttpRequest();
  req.onreadystatechange= function(){
    if (this.readyState == 4 && this.status == 200){
      var data = JSON.parse(this.responseText);
      table_div.setAttribute("hidden","")
      edit_section.removeAttribute("hidden")
      name_.value=data.name
      nickname.value=data.nickname
      phone_number.value=data.phone_number
      address.value=data.address
      work.value=data.work
      email.value=data.email
      notes.value=data.notes

      var group_text="";
      for (i in data.group_list){
        group_text+="<option>"+data.group_list[i]+"</option>"
      group_list.innerHTML = group_text;
      }
    }
  }
  req.open("POST" , "edit" , true)
  req.setRequestHeader("content-type", "application/json")
  req.send(JSON.stringify(api))
}
/*### all table tr onclick event , with ajax - return query result###*/

/*##filter field event with ajax return result##*/
filter.oninput = function (){
  try{ // i used 'try' because this element is not be created yet
      flash_message.innerHTML="" //remove last flash message
  }catch{}

  table_div.removeAttribute("hidden")
  edit_section.setAttribute("hidden","")
  var req = new XMLHttpRequest();
  api.case="filter"
  api.filter=filter.value
  for (i in filter_by){
    if (filter_by[i].checked){
      api.filter_by = filter_by[i].value;
    }
  }
  req.onreadystatechange = function (){
    if (this.readyState == 4 && this.status == 200){
      data = JSON.parse(this.responseText)
      res_table.innerHTML=data.html
      var tr = document.getElementsByTagName("tr");
      for (var i=0;i<tr.length;i++){
        tr[i].addEventListener('click',function(event){
          id_value.value = event.target.id //set query id to send with form
          api["case"] ="edit"
          api["id"] = event.target.id
          var req = new XMLHttpRequest();
          req.onreadystatechange= function(){
            if (this.readyState == 4 && this.status == 200){
              var data = JSON.parse(this.responseText);
              table_div.setAttribute("hidden","")
              edit_section.removeAttribute("hidden")
              name_.value=data.name
              nickname.value=data.nickname
              phone_number.value=data.phone_number
              address.value=data.address
              work.value=data.work
              email.value=data.email
              notes.value=data.notes

              var group_text="";
              for (i in data.group_list){
                group_text+="<option>"+data.group_list[i]+"</option>"
              group_list.innerHTML = group_text;
              }
            }
          }
          req.open("POST" , "edit" , true)
          req.setRequestHeader("content-type", "application/json")
          req.send(JSON.stringify(api))
        })
      }
    }
  }
  req.open("POST" , "edit" , true)
  req.setRequestHeader("content-type", "application/json")
  req.send(JSON.stringify(api))
}
/*##END -- filter field event with ajax  return result##*/

/*##Cancle Button event##*/
cancle_button.onclick = function (){
    table_div.removeAttribute("hidden");;
    edit_section.setAttribute("hidden", "");
}
/*##END --Cancle Button event##*/

/*##new group checkbox event##*/
group_checkbox.onchange = function (){
  if (group_checkbox.checked){
    new_group_flag.value = "1"
    group_list.setAttribute("disabled", "")
    group_text.removeAttribute("disabled")
    groups_rules.value = group_text.value
  }else {
    new_group_flag.value = "0"
    group_list.removeAttribute("disabled")
    group_text.setAttribute("disabled", "")
    groups_rules.value =group_list.value
  }
}
/*##END -- new group checkbox event##*/

/*##When click on update button will determine group value taken from group_text or group_list##*/
update_button.onmouseover  = function (){
  if (new_group_flag.value == "1"){
    groups_rules.value = group_text.value
  }else{
    group_list.options[group_list.selectedIndex].value
  }
}
/*##END -- When click on update button will determine group value taken from group_text or group_list##*/

/*##Change Flash Massege Color Depend on it case##*/
window.onload = function () {
  try{
      if (flash_message.innerHTML=="You didn't change any value on This Record"){
        flash_message.setAttribute("style","color:blue")
      }else if (flash_message.innerHTML=="Record Updated successfully"){
        flash_message.setAttribute("style","color:green")
      }else{
        flash_message.setAttribute("style","color:red")
      }
  }catch{}

}
/*##END -- Change Flash Massege Color Depend on it case##*/
