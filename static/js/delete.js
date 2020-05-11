//HTML element varibales
var filter = document.getElementById("filter"),
    filter_by = document.getElementsByName("filter_by"),
    one_by_one = document.getElementById("one_by_one"),
    mark = document.getElementById("mark"),
    delete_button = document.getElementById("delete_button"),
    delete_all = document.getElementById("delete_all"),
    res_table = document.getElementById("res_table"),
    selected_id=document.getElementById("selected_id"); //hidden

/*##api structure##*/
api={
  case:"",//default if [no selection]
  filter:"",
  filter_active:"1",
  filter_by:"name",//default if [no selection]
  selected_id :[],
  html:""
}
/*##END -- api structure##*/

/*##get radio button value on click event and put it in API object##*/
for (var i=0;i<filter_by.length;i++){
  filter_by[i].addEventListener('click',function(event){
    api.filter_by=event.target.value
  })
}
/*##END -- get radio button value on click event and put it in API object##*/

/*##change between two style for an element ##*/
function button_style_change (element , on_off){
  if (on_off == "on"){
    element.style.boxShadow="0px 0px 10px 5px #51ECFF";
    element.style.backgroundColor="#5195FF";
    element.style.color = "white";
  }else if (on_off == "off") {
    element.style.boxShadow="none";
    element.style.backgroundColor="lightgray";
    element.style.color = "black";
  }
}
/*##END -- change between two style for an element ##*/

/*##build event for button  in table for 'deleteing'##*/
function delete_buttons_event(){
  var selection_element = document.getElementsByName("delete_row")
  for (var i=0;i<selection_element.length;i++){
    selection_element[i].addEventListener('click', function (event){
      api.selected_id.push(event.target.id) //to send to server what id we want to delete
      var row = document.getElementsByName("rows");
      api.case="delete_one"
      req = new XMLHttpRequest();//this request will do delete on selected row in database
      req.onreadystatechange = function (){
        if (this.readyState == 4 && this.status == 200){
          data = JSON.parse(this.responseText)//not used - for testing only
        }
      }
      req.open("POST","delete",true)
      req.setRequestHeader("content-type", "application/json")
      req.send(JSON.stringify(api))

      for (var i=0;i<row.length;i++){
        if (row[i].id == event.target.id){
          row[i].parentNode.removeChild(row[i])
        }
      }
    })
  }
}
/*##END -- build event for button in table for 'deleteing'##*/

/*##build event for Mark 'checkbox' in table for 'deleteing multi record'##*/
function delete_mark_event(){
  var selection_element = document.getElementsByName("checkbox_row")
  for (var i=0;i<selection_element.length;i++){
    selection_element[i].addEventListener('click', function (event){
      if (event.target.checked) {
        api.selected_id.push(event.target.id)
      }else if (event.target.checked == false){
        for (i in api["selected_id"]){
          if (api["selected_id"][i] == event.target.id ){
            api.selected_id.splice(i,1)
            }
          }
        }
      //get rows for change its color when marked
      var rows = document.getElementsByName("rows");
      for (var i=0;i<rows.length;i++){
        if (rows[i].id == event.target.id && event.target.checked){
          rows[i].style.backgroundColor="#ff2c2c"
          rows[i].style.color="white"
        }else if (rows[i].id == event.target.id && event.target.checked == false){
          rows[i].style.backgroundColor="inherit"
          rows[i].style.color="inherit"
        }
      }
      if (api.selected_id.length > 0){//show or hide delete button depend on 'marks'
        delete_button.removeAttribute("disabled")
      }else if (api.selected_id.length == 0){
        delete_button.setAttribute("disabled","")
      }
    })
  }
}
/*##END -- build event for Mark 'checkbox' in table for 'deleteing multi record'##*/

/*## 'one by one' button Event Action */
one_by_one.addEventListener('click',function (){
  delete_button.setAttribute("hidden","")
  delete_button.setAttribute("disabled","")
  button_style_change(one_by_one,"on")
  button_style_change(mark,"off")
  var req = new XMLHttpRequest();
  api["selected_id"]=[]//clear id selected from last action
  api.case="one_by_one"
  req.onreadystatechange = function (){
    if(this.readyState == 4 && this.status == 200){
      data = JSON.parse(this.responseText)
      res_table.innerHTML = data.html //will draw table with database data
      delete_buttons_event() //will add event to delete buttons on table
      }
    }
  req.open("POST","delete",true)
  req.setRequestHeader("content-type", "application/json")
  req.send(JSON.stringify(api))
})
/*##END --  'one by one' button Event Action */

/*## 'mark' button Event Action */
mark.addEventListener('click',function (){
  delete_button.setAttribute("disabled","")
  delete_button.removeAttribute("hidden")
  button_style_change(one_by_one,"off")
  button_style_change(mark,"on")
  api["selected_id"]=[]//clear id selected from last action
  api.case="mark"
  var req = new XMLHttpRequest();
  req.onreadystatechange = function (){
    if(this.readyState == 4 && this.status == 200){
      data = JSON.parse(this.responseText)
      res_table.innerHTML = data.html
      delete_mark_event()
    }
  }
  req.open("POST","delete",true)
  req.setRequestHeader("content-type", "application/json")
  req.send(JSON.stringify(api))
})
/*##END 'mark' button Event Action */

/*## 'delete_all' button Event Action */
delete_all.addEventListener('click',function (){
  last_case = api["case"]
  var assert_delete = prompt("You are about to delete all record !!!\n Type 'OK' in capital ")
  if (assert_delete == "OK"){
    delete_button.setAttribute("disabled","")
    api.case="delete_all"
    var req = new XMLHttpRequest();
    req.onreadystatechange = function (){
      if(this.readyState == 4 && this.status == 200){
        data = JSON.parse(this.responseText)
        res_table.innerHTML = data.html
      }
    }
    req.open("POST","delete",true)
    req.setRequestHeader("content-type", "application/json")
    req.send(JSON.stringify(api))
    alert("ALL RECORD DELETED SUCCESSFULLY")
  }else{
    alert("Failed To Delete Records")
  }
})
/*##END -- 'delete_all' button Event Action */

/*##'filter' field Event Action [on input ]*/
filter.addEventListener('input', function (event){
  if (api["case"]==""){
      api["case"]="one_by_one"
  }
  api["filter"] = filter.value;
  api["selected_id"]=[] //clear id selected from laste action

  if(api["case"]=="delete_one"){
    api["case"] ="one_by_one"
  }else if (api["case"]=="marked_row"){
    api["case"] ="mark"
  }
  var req = new XMLHttpRequest();
  req.onreadystatechange = function (){
    if (this.readyState == 4 && this.status == 200){
      data =JSON.parse(this.responseText)
      res_table.innerHTML = data.html
      delete_buttons_event() //will add event to delete buttons on table
      delete_mark_event()
    }
  }
  req.open("POST","delete",true)
  req.setRequestHeader("content-type", "application/json")
  req.send(JSON.stringify(api))
})
/*##END -- 'filter' field Event Action [on input ]*/

/*##the first page 'delete button event'##*/
var delete_row = document.getElementsByName("delete_row")
for (var i=0;i<delete_row.length;i++){
  delete_row[i].addEventListener('click', function (){
    api.selected_id.push(event.target.id)
    var row = document.getElementsByName("rows");
    for (var i=0;i<row.length;i++){
      if (row[i].id == event.target.id){
        row[i].parentNode.removeChild(row[i])
      }
    }
    api.case="delete_one"
    req = new XMLHttpRequest();//this request will do delete on selected row in database
    req.onreadystatechange = function (){
      if (this.readyState == 4 && this.status == 200){
      }
    }
    req.open("POST","delete",true)
    req.setRequestHeader("content-type", "application/json")
    req.send(JSON.stringify(api))
  })
}
/*##END -- the first page 'delete button event'##*/

/*Delete Button event onclick*/
delete_button.onclick = function (){
  delete_mark_event()
  api.case="marked_row"//for api
  //delete selected row after before request send to server
  var checked_rows = document.getElementsByName("checkbox_row"),
      table_row =document.getElementsByName("rows"),
      selected_from_table=[];
  for (var i=0;i<checked_rows.length;i++){
    if (checked_rows[i].checked) {
      selected_from_table.push(checked_rows[i].id)//put ids into array to use it latter for deleting rows
    }
  }
  //deleteing rows
  var element;
  for (i in selected_from_table){
    var element = document.getElementById(selected_from_table[i]);
    element.parentNode.removeChild(element)
  }
  delete_button.setAttribute("disabled","")

  req = new XMLHttpRequest();
  req.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200){
      this.responseText
    }
  }
  req.open("POST" , "delete" , true)
  req.setRequestHeader("content-type", "application/json")
  req.send(JSON.stringify(api))
}
