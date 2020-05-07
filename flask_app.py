#Start Date : 28/04/2020
#Died line : expected  30 days or less
#Pure JS coding [No Jquery], Pure SQL coding [No ORM]

from flask import Flask , render_template , redirect , url_for , request , send_file , flash , jsonify , Response
import actions , os , json , time

#decomment the next line in server [pythonanywhere.com] to fix path problem
# os.chdir(os.getcwd()+"/mysite/")

db=actions.database("database/phone_app_db.db")
api=actions.api("database/phone_app_db.db")

app=Flask(__name__)
app.secret_key = b'\x06\x03\x02cA\x04\x15@'
app.config['TEMPLATES_AUTO_RELOAD'] = True  #fix caching problem with pythonanywhere.com


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

###################################
############ WORK AREA ############
###################################

@app.route("/groups" , methods=["GET","POST"])
def groups_ (summary=None):
    'Groups Page'
    groups = db.query_statment("select * from groups_")#query groups first then put them in all select elements
    if request.method == "POST":
        try : # for ajax
            ajax = request.get_json()
            if ajax["case"] == "update_summary":
                summary = db.mange_group(request_json=ajax)["summary"]
                return jsonify(summary)
        except : # for form
            form_api = json.loads(request.form.get("add_api"))
            form_data = db.mange_group (request_form=request.form.get)
            if form_api["case"] =="rename" :
                flash(form_data["rename"])
                return render_template("groups.html",summary=form_data["summary"] , groups = groups)
            elif form_api["case"] == "create_new":
                #flash(form_data["rename"])
                #return render_template("groups.html",summary=form_data["summary"] , groups = groups)
                return "DONE"
            else:
                return "else"

    summary  = db.edit_groups()
    return render_template("groups.html",summary=summary , groups = groups)

##########################################
############ END -- WORK AREA ############
##########################################


@app.route("/backup_and_restore")
def backup_restore_ ():
    return render_template("backup_and_restore.html")


@app.route("/about")
def about_ ():
    'About Page'
    return render_template("about.html")

@app.route("/gpl3")
def gpl3_ ():
    'License Page'
    return render_template("gpl3.html")#i didnt create this template - i copied it from web

@app.route("/download")#make user download file
def send_project_file ():
    return send_file("files/mysite.zip" , as_attachment=True)



#run server
if __name__ =="__main__":
    app.run()
