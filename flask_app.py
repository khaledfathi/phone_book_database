#Start Date : 28/04/2020
#Died line : expected  30 days or less
#Pure JS coding [No Jquery], Pure SQL coding [No ORM]

#END ON 11/05/2020 [14 days] avg hours each day 9hr [max 13hr , min 5hr]#

from flask import Flask , render_template , redirect , url_for , request , send_file , flash , jsonify , Response
import actions , os , json , time , shutil

#decomment the next line in server [pythonanywhere.com] to fix path problem
#os.chdir(os.getcwd()+"/mysite/")

db=actions.database("database/phone_app_db.db")
db.other_database("database/history.db","create")
api=actions.api("database/phone_app_db.db")

UPLOAD_FOLDER="uploads/"
ALLOWED_EXTENTIONS={"db"}

app=Flask(__name__)
app.secret_key = b'\x06\x03\x02cA\x04\x15@'
app.config['TEMPLATES_AUTO_RELOAD'] = True  #fix caching problem with pythonanywhere.com
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.config['DOWNLOAD_PATH'] ="files/mysite.zip"


@app.route("/")
def index ():
    'Home Page'
    return render_template("index.html")

@app.route("/search" , methods=["GET" , "POST"])
def search_ (results=None , no_results=None):
    'Search Page'
    groups = db.query_statment("select * from groups_")#it will REFERENCE groups from database to frontend group list
    if request.method == "POST":
        form_data =db.qurey(request.form.get("query") ,\
         request.form.get("query_rules") ,\
         request.form.get("general_search_flag"))
        results = db.query_statment(form_data)
        if not results :
            no_results = "There is No Match Data Found"
        return render_template("search.html" , result=results , no_results=no_results , groups=groups )
    return render_template("search.html" , result=results , no_results=no_results , groups=groups )

@app.route("/add" , methods=["GET" , "POST"])
def add_ (msg=None):
    'Add Page'
    groups = db.query_statment("select * from groups_")
    if request.method == "POST" :
        if (db.new_record(request.form.get)) : #this method do everything to new record
            flash("Record Saved")
            return redirect(url_for("add_"))
        else :
            return render_template("add.html" , groups = groups , group_error =" you are entered an existing Data in DataBase | check [name , phone number , new group]")
    return render_template("add.html" , groups = groups )

@app.route("/edit" , methods=["GET" , "POST"])
def edit_ ():
    'Edit Page'
    if request.method == "POST" :
        try:#AJAX requests
            req_api = request.get_json()
            if req_api["case"] == "edit":
                return jsonify(api.show_row_to_edit(req_api))
            elif req_api["case"] == "filter":
                return jsonify(api.filter(req_api))
        except :#Form requests
            if (db.update_record(request.form.get)) == "updated":
                flash("Record Updated successfully")
                return redirect(url_for("edit_"))
            elif (db.update_record(request.form.get)) == "same_values":
                flash("You didn't change any value on This Record")
                return redirect(url_for("edit_"))
            elif (db.update_record(request.form.get)) == "duplicated":
                flash("Record Update Failed : Duplicate Data")
                return redirect(url_for("edit_"))
    result = db.query_all_for_edit_page()
    return render_template("edit.html" , result = result)

@app.route("/delete" , methods=["GET","POST"])
def delete_ ():
    'Delete Page'
    if request.method == "POST":
        req_api=request.get_json()
        print (req_api)
        if req_api["case"] == "one_by_one" or  req_api["case"] == "mark":
            return jsonify(api.delete_type(req_api))
        elif req_api["case"] in ["marked_row" , "delete_one" , "delete_all"] :
            return jsonify(api.delete_action(req_api))
        else:
            return "check cases in api" # DEBUG:
    result = db.query_all_for_delete_page()
    return render_template("delete.html" , result=result)

@app.route("/groups" , methods=["GET","POST"])
def groups_ (summary=None):
    'Groups Page'
    if request.method == "POST":
        try : # for ajax
            ajax = request.get_json()
            if ajax["update_summary"] == "1":
                summary = db.mange_group(request_json=ajax)["summary"]
                return jsonify(summary)
        except : # for form
            form_data = db.mange_group (request_form=request.form.get)
            print (form_data)
            form_api = json.loads(request.form.get("add_api"))
            if form_api["case"] =="rename" and form_api["create_new"]=="0":
                flash(form_data["rename"])
                return redirect(url_for("groups_"))
            elif form_api["case"] == "rename" and form_api["create_new"]=="1":
                flash(form_data["create_new"])
                return redirect(url_for("groups_"))
            elif form_api["case"] == "remove" :
                flash(form_data["remove"])
                return redirect(url_for("groups_"))
            else:
                return redirect(url_for("groups_"))
    summary  = db.edit_groups()
    groups = db.query_statment("select * from groups_")
    return render_template("groups.html",summary=summary , groups = groups)

@app.route("/backup_and_restore" , methods=["GET", "POST"])
def backup_restore_ ():
    if request.method == "POST" :
        form_case=request.form.get("import_export_flag")
        if form_case =="export" :##########
            app.config['DOWNLOAD_PATH']= actions.export_file(request.form.get("export_file_type") )
            return redirect(url_for("download_"))
        elif form_case == "import":
            file_ = request.files['import_file']
            if file_.filename == '':
                flash("Error : You did not select any file")
                return redirect(url_for("backup_restore_"))
            elif file_ and actions.allowed_file(file_.filename , ["db"]):
                import_file = request.files["import_file"]
                import_file.save(os.path.join(app.config["UPLOAD_FOLDER"],"testing.db"))
                if actions.import_file(db) :
                    flash("File Imported")
                    return redirect(url_for("backup_restore_"))
                else :
                    flash("Error : database File is not compatible")
                    return redirect(url_for("backup_restore_"))
            elif file_ and not actions.allowed_file(file_.filename , ["db"]):
                flash("Error : File Type Not Allowed | select '.db' file only")
                return redirect(url_for("backup_restore_"))
        elif request.data.decode() =="backup" :
            resp =jsonify(db.backup())
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        elif request.data.decode() == "restore":
            resp =jsonify(db.restore())
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp

    history = db.history_update()
    last_backup_restore = db.last_backup_restore ()
    last_import=actions.last_import(db)
    last_export=actions.last_export(db)
    return render_template("backup_and_restore.html" , history=history ,last_backup_restore = last_backup_restore , last_import=last_import , last_export=last_export)

@app.route("/about")
def about_ ():
    'About Page'
    return render_template("about.html")

@app.route("/gpl3")
def gpl3_ ():
    'License Page'
    return render_template("gpl3.html")#i didnt create this template - i copied it from web

@app.route("/download")#make user download file
def download_ ():
     return send_file(app.config['DOWNLOAD_PATH'] , as_attachment=True)



#run server
if __name__ =="__main__":
    app.run()
