/*############################*/
/*### FILE FOR ADD PAGE ###*/
/*############################*/

/*##General Element variable ##*/
var name_ = document.getElementById("name_"),
    nickname = document.getElementById("nickname"),
    phone_number = document.getElementById("phone_number"),
    address = document.getElementById("address"),
    work = document.getElementById("work"),
    email = document.getElementById("email"),
    notes = document.getElementById("notes"),
    group_list = document.getElementById("group_list"),
    group_text = document.getElementById("group_text"),
    group_checkbox = document.getElementById("group_checkbox"),
    clear_button = document.getElementById("clear_button"),
    save_button = document.getElementById("save_button"),
    groups_rules = document.getElementById("groups_rules"),
    new_group_flag = document.getElementById("new_group_flag");


/*##END -- General Element variable ##*/

/*##Change Group Mode [select or new one]##*/
group_checkbox.onclick = function (){
  if ( group_checkbox.checked ){
    group_list.setAttribute("disabled", "");
    group_text.removeAttribute("disabled")
  }else{
    group_text.setAttribute("disabled", "");
    group_list.removeAttribute("disabled")  }
}
/*##END -- Change Group Mode [select or new one]##*/

/*## Clear Field Button Action */
clear_button.onclick = function (){
  name_.value = "";
  nickname.value = "";
  phone_number.value = "";
  phone_number.value ="";
  address.value = "";
  work.value = "";
  email.value = "";
  notes.value = "";
  group_list.selectedIndex=0;
  group_text.value = "";
}
/*##END -- Clear Field Button Action */

/*##1-Determine group data to send to the server with form ##*/
/*##2-flag to  Determine the group data [is it new or not ]##*/
save_button.onclick = function () {
  if (group_checkbox.checked ){
    groups_rules.value =group_text.value;
    new_group_flag.value = 1;
  }else{
    groups_rules.value = group_list.options[group_list.selectedIndex].text;
    new_group_flag.value = 0;
  }
}
/*##END -- 1- Determine group data to send to the server with form ##*/
/*##END -- 2- flag to  Determine the group data [is it new or not ]##*/
