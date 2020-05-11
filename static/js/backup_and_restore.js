//HTML ELEMENTS
var backup_button =document.getElementById("backup_button"),
    restore_button =document.getElementById("restore_button"),
    backup_date_time = document.getElementById("backup_date_time"),
    restore_date_time = document.getElementById("restore_date_time"),
    history_table =document.getElementById("history_table"),
    import_export_flag = document.getElementById("import_export_flag")
    import_button = document.getElementById("import_button"),
    export_button = document.getElementById("export_button"),
    export_type_selected =document.getElementById("export_type_selected"),
    export_file_type = document.getElementById("export_file_type");


//api
var api = {
  case:""
}

backup_button.onclick = function (){
  var req= new XMLHttpRequest();
  req.onreadystatechange = function (){
    if (this.readyState == 4 && this.status == 200){
      data = JSON.parse(this.responseText)
      backup_date_time.innerHTML = "Last Backup : " + data.last_info
      history_table.innerHTML = data.table
      alert("Database is Backedup")
    }
  }
  req.open("POST","backup_and_restore", true)
  req.setRequestHeader("Content-Type", "text/plain")
  req.send("backup")
}

restore_button.onclick = function (){
  var req= new XMLHttpRequest();
  req.onreadystatechange = function (){
    if (this.readyState == 4 && this.status == 200){
      data = JSON.parse(this.responseText)
      restore_date_time.innerHTML = "Last Restore : " + data.last_info
      history_table.innerHTML = data.table
      alert("Database is Restored")
    }
  }
  req.open("POST","backup_and_restore", true)
  req.setRequestHeader("Content-Type", "text/plain")
  req.send("restore")
}

/*import export button actions*/
import_button.onclick = function (){
  import_export_flag.value = "import"
}
export_button.onclick = function (){
  import_export_flag.value="export"
  export_file_type.value = export_type_selected.options[export_type_selected.selectedIndex].innerText
}
