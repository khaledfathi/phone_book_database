/*############################*/
/*### FILE FOR SEARCH PAGE ###*/
/*############################*/

/*## general element variable ##*/
var advanced_search_button = document.getElementById("advanced_search_button")
  advanced_search_block = document.getElementById("advanced_search_block"),
  result_data = document.getElementById("result_data"),
  search_input = document.getElementById("search_input"),
  search_by = document.getElementById("search_by") ,
  pattern = document.getElementById("pattern"),
  order = document.getElementById("order"),
  groups = document.getElementById("groups"),
  submit = document.getElementById("submit"),
  general_search_flag = document.getElementById("general_search_flag");
/*##END-- general element variable ##*/

/*##Advanced Search On/OFF [ show or hide filters ]##*/
advanced_search_button.onclick = function (){
  if (advanced_search_block.getAttributeNode("hidden") ){
    general_search_flag.value=1 //tell server to search with rules
    advanced_search_block.removeAttribute("hidden");
    result_data.style.height = "65%"
  }else{
    general_search_flag.value=0 //tell server to search with NO rules
    advanced_search_block.setAttribute("hidden","");
    result_data.style.height = "80%"
    search_by.selectedIndex=0;
    pattern.selectedIndex=0;
    order.selectedIndex = 0;
    groups.selectedIndex=0;
    search_input.setAttribute("placeholder", search_by.options[search_by.selectedIndex].text)
  }
}
/*##END--- Advanced Search On/OFF##*/

/*##Change Search placeholder depend on filters##*/
search_by.onchange = function (){
  var value_of_filter = search_by.options[search_by.selectedIndex].text;
  switch (value_of_filter) {
    case "Name":
    search_input.setAttribute("placeholder", "Name");
    break;
    case "Nickname" :
    search_input.setAttribute("placeholder", "Nickname");
    break;
    case "Phone_Number" :
    search_input.setAttribute("placeholder", "Phone");
    break;
    case "Address" :
    search_input.setAttribute("placeholder", "Address");
    break;
    case "Work" :
    search_input.setAttribute("placeholder", "Work");
    break;
    case "Email" :
    search_input.setAttribute("placeholder", "Email");
    break;
    case "Note" :
    search_input.setAttribute("placeholder", "Note");
    break;
  }
}
/*##END -- Change Search placeholder depend on filters##*/


/*## collect search rules in hidden input ##*/
var query_rules = document.getElementById("query_rules");

function get_rules (){
  query_rules.value = search_by.options[search_by.selectedIndex].innerHTML+","+
  pattern.options[pattern.selectedIndex].innerHTML+","+
  order.options[order.selectedIndex].innerHTML+","+
  groups.options[groups.selectedIndex].innerHTML
}

submit.onclick  = function (){
  get_rules()
}
/*##END -- collect search rules in hidden input ##*/
