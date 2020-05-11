#main Actions lib
import sqlite3 , json , datetime , shutil , os

class database :
    "data base controller class"
    def __init__ (self,db_file):
        'init function'
        self.db_file=db_file #path of new database file
        self.create_db()

    def sql (self,statment):
        "execute sql statments and commit it direct to database"
        with sqlite3.connect(self.db_file) as conn :
            cur = conn.cursor()
            cur.execute(statment)
            conn.commit()

    def create_db (self):
        'create two tables [groups_ and phone_book]'
        self.sql("PRAGMA foreign_key = on")
        self.sql("CREATE TABLE IF NOT EXISTS groups_ (group_ text primary key)")
        self.sql("""
        CREATE TABLE IF NOT EXISTS phone_book (
          id integer primary key autoincrement ,
          name text  unique ,
          nickname text ,
          phone_number text,
          address text ,
          work text ,
          email text ,
          notes text ,
          group_ text  default 'default' ,
          foreign key (group_) REFERENCES groups_(group_)
        );
        """)
        try :
            self.sql("INSERT INTO groups_ VALUES ('default')")
        except :
            pass

    def query_all(self,table):
        'return all data in the table/s'
        with sqlite3.connect(self.db_file) as conn :
            cur = conn.cursor()
            cur.execute("SELECT * FROM "+table)
            return cur.fetchall()

    def query_statment(self,statment):
        'return result of query depend on statment [used for query only]'
        with sqlite3.connect(self.db_file) as conn :
            cur = conn.cursor()
            cur.execute(statment)
            return cur.fetchall()

    def qurey (self, query , query_rules , general_search_flag):
        "convert rules from html element , to one sql statment for query "
        query_rules =  query_rules.split(",")
        query_rules={\
        "search_by":query_rules[0],\
        "pattern":query_rules[1],\
        "order":query_rules[2],\
        "groups":query_rules[3]}
        final_statment = "select name , Nickname , phone_number ,\
         address , work , email , notes, group_\
          from phone_book where "+query_rules["search_by"]+" "
        if query_rules["pattern"] == "Contains":
            final_statment+="like \'%"+query+"%\' and group_= \'"+query_rules["groups"]+"\' "
        elif query_rules["pattern"] == "Start With":
            final_statment+="like \'"+query+"%\' and group_=  \'"+query_rules["groups"]+"\' "
        elif query_rules["pattern"] == "End With":
            final_statment+="like \'%"+query+"\' and group_= \'"+query_rules["groups"]+"\' "
        elif query_rules["pattern"] == "Equal":
            final_statment+="=\'"+query+"\' and group_= \'"+query_rules["groups"]+"\' "

        if query_rules["order"] == "Ascending":
            final_statment+="order by name ASC"
            order="asc"
        elif query_rules["order"] == "Descending":
            final_statment+="order by name DESC"
            order="desc"

        if not query:
            no_data= """
            select * from phone_book where phone_book.Name =''
            and group_='' order by name ASC"""
            return no_data
        elif query == "*all*" : #query all table
            return "select name , Nickname , phone_number ,\
             address , work , email , notes, group_ from phone_book order by name "+order
        elif general_search_flag == "0": #default search criteria is search by character with no rules
            print ("aaaa")
            return "SELECT name , nickname , phone_number , address , work , \
            email , notes , group_ FROM phone_book where name like \'%" +query+"%\'"
        return final_statment

    def new_record (self, request_form_get):
        'new record in tables'
        data_label =["name","nickname","phone_number","address","work","email","notes","group","new_group_flag"]
        data_values = [request_form_get(i) for i in data_label]
        data_dic={}
        for key , i in enumerate(data_values) :
            data_dic[ data_label[key] ]=i.strip()
        #if new group - add this group in groups table first , then record all new data
        if data_dic["new_group_flag"] == "1":
            #check duplicated entry group with database
            if self.query_statment("select * from groups_ where group_ = '{}'".format(data_dic["group"])):
                return False
            self.sql("INSERT INTO groups_ VALUES ('{}')".format(data_dic["group"]))#record new group first
            self.sql("INSERT INTO phone_book (name , nickname , phone_number , address , work , email , notes , group_)\
             VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}' )".\
             format(data_dic["name"],\
             data_dic["nickname"],\
             data_dic["phone_number"],\
             data_dic["address"],\
             data_dic["work"],\
             data_dic["email"],\
             data_dic["notes"],\
             data_dic["group"]) )
        else : # do the record
            #check duplicated entry [name , phone_number] with database (because they're unique in database)
            if self.query_statment("SELECT * FROM phone_book where name = '{}'".format(data_dic["name"])) or \
            self.query_statment("SELECT * FROM phone_book where phone_number = '{}'".format(data_dic["phone_number"])):
                return False
            self.sql("INSERT INTO phone_book (name , nickname , phone_number , address , work , email , notes , group_)\
             VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}' )".\
             format(data_dic["name"],\
             data_dic["nickname"],\
             data_dic["phone_number"],\
             data_dic["address"],\
             data_dic["work"],\
             data_dic["email"],\
             data_dic["notes"],\
             data_dic["group"]) )
        return True #important to prevent  duplicated error

    def update_record (self,request_form_get):
        'new update in tables'
        data_label =["name","nickname","phone_number","address","work","email","notes","group","new_group_flag","id_value"]
        data_values = [request_form_get(i) for i in data_label]
        data_dic={}
        for key , i in enumerate(data_values) :
            data_dic[ data_label[key] ]=i.strip()

        def check_this_row():
            "Nested Function that do : check if update is same as the original record"
            if self.query_statment("SELECT * FROM phone_book WHERE name ='{}' and nickname='{}' and phone_number='{}' and address='{}' and work='{}' and email='{}' and notes='{}' and group_='{}' ".format(\
            data_dic["name"],\
            data_dic["nickname"],\
            data_dic["phone_number"],\
            data_dic["address"],\
            data_dic["work"],\
            data_dic["email"],\
            data_dic["notes"],\
            data_dic["group"]) ) : return True
            else :
                return False
        def update ():
            self.sql("UPDATE phone_book SET name ='{}' , nickname='{}' , phone_number='{}' , address='{}' , work='{}' , email='{}' , notes='{}' , group_='{}' where id = {}".format(\
            data_dic["name"],\
            data_dic["nickname"],\
            data_dic["phone_number"],\
            data_dic["address"],\
            data_dic["work"],\
            data_dic["email"],\
            data_dic["notes"],\
            data_dic["group"],\
            data_dic["id_value"]))
        #if new group - add this group in groups table first , then record all new data
        if data_dic["new_group_flag"] == "1":
            #check duplicated entry group with database
            if self.query_statment("select * from groups_ where group_ = '{}'".format(data_dic["group"])):
                if check_this_row() :#check if update is same as the original record
                    self.query_statment("DELETE groups_ where group_ = '{}'".format(data_dic["group"]))
                    return "same_values"
                return "duplicated"
            #UPDATE phone_book SET name="hassan22222" where id =3
            self.sql("INSERT INTO groups_ VALUES ('{}')".format(data_dic["group"]))#record new group first
            try: #try to insert data in table , return 'duplicated' to indicate if any data is duplicated
                update()
            except:
                return "duplicated"
            return "updated"
        else : # do the record
            if check_this_row() : return "same_values"#check if update is same as the original record
            try: #try to insert data in table , return 'duplicated' to indicate if any data is duplicated
                update()
            except:
                return "duplicated"
        return "updated" #important to prevent  duplicated error

    def query_all_for_edit_page (self):
        'query all data from phone_book table then put \
        result rows as html [tr] then save it in include.html , to show it as default in edit page'
        data = self.query_all("phone_book")
        html="""
        <thead>
            <td>Name</td>
            <td>Nickname</td>
            <td>Phone Number</td>
            <td>Address</td>
            <td>Work</td>
            <td>Email</td>
            <td>Notes</td>
            <td>Group</td>
        </thead>
        """
        for rows in data :
            html+="<tr>"
            for cells in rows[1:] :
                html+= "<td id='"+str(rows[0])+"'>" + str(cells) + "</td>"
            html+="</td>"
        with open("templates/includes/include_edit_page.html","w") as f :
            f.write(html)
        return True

    def query_all_for_delete_page (self):
        "use as a main result table , it will be first render for 'delete page' "
        data = self.query_all("phone_book")
        html="""
        <thead>
            <td>Name</td>
            <td>Nickname</td>
            <td>Phone Number</td>
            <td>Address</td>
            <td>Work</td>
            <td>Email</td>
            <td>Notes</td>
            <td>Group</td>
            <td>Mark</td>
        </thead>
        """
        for rows in data :
            html+="<tr name='rows' id='"+str(rows[0])+"'>"
            for cells in rows[1:] :
                html+= "<td id='"+str(rows[0])+"'>" + str(cells) + "</td>"
            html+="</td><td><button id="+str(rows[0])+" name='delete_row'>Delete</button></td>"
        with open("templates/includes/include_delete_page.html","w") as f :
            f.write(html)
        return True

    def edit_groups (self , group='default'):
        'get summary for summary page'
        res=[]
        #count groups
        res.append(str(self.query_statment("SELECT count(group_) FROM groups_")[0][0]))
        #count contacts in group
        res.append(str(self.query_statment("SELECT count(name) FROM phone_book WHERE group_ ='%s'"% group)[0][0]))
        #count all contacts in group
        res.append(str(self.query_statment("SELECT count(name) FROM phone_book")[0][0]))
        return res

    def mange_group(self,request_form=False  , request_json=False):###########################
        results={} #will return every thing from this function
        form_dic={} #data from form formated
        if  request_form : #sent by form
            elements=["rename_field","new_group_text","remove_move_to_new","add_api"]
            for i in elements :
                form_dic[i] = request_form(i)
            form_dic["add_api"] = json.loads(form_dic["add_api"])
            results["form_dic"]=form_dic #save form data in result dictionary to use it in return
            results["summary"]= self.edit_groups(form_dic["add_api"]["selected_group"]) # data for summary table
            if form_dic["add_api"]["case"] =="rename" and form_dic["add_api"]["create_new"]=="0":#case rename group
                if not form_dic["rename_field"]:
                    results["rename"] ="Nothing Changed : Empty Field"
                elif  form_dic['add_api']["selected_group"].casefold() == 'default':
                    results["rename"] ="Error : You cant Edit 'default' Group"
                else :
                    if self.query_statment("SELECT * FROM groups_ Where group_='%s'"%form_dic["rename_field"]) :
                        results["rename"] ="Nothing Change : Duplicated Group Name"
                    else:
                        self.sql("INSERT INTO groups_ VALUES ('{}')".format(form_dic["rename_field"]) ) # creat new group
                        self.sql("UPDATE phone_book SET group_='{}' WHERE group_='{}'".format(form_dic["rename_field"] , form_dic["add_api"]["selected_group"])) #copy old contact to new group
                        self.sql("DELETE FROM groups_ WHERE group_='{}'".format(form_dic["add_api"]["selected_group"]) ) #delete old group
                        results["rename"] ="Group Renamed"
            elif form_dic["add_api"]["case"] =="rename" and form_dic ["add_api"]["create_new"]=="1": # case create new group
                if not form_dic["new_group_text"] :
                    results["create_new"] ="Nothing Changed : Empty Field"
                elif form_dic["new_group_text"].casefold() == "default":
                    results["create_new"] ="name 'default is not allowed'"
                elif self.query_statment("SELECT * FROM groups_ Where group_='%s'"%form_dic["new_group_text"]) :
                    results["create_new"] ="Nothing Change : Duplicated Group Name"
                else:
                    self.sql("INSERT INTO groups_ VALUES ('{}')".format(form_dic["new_group_text"]) ) # creat new group
                    results["create_new"] = "New Group Created"
            elif form_dic["add_api"]["case"] == "remove": #####################3
                if form_dic["add_api"]["remove_option"] == "opt1":
                    if form_dic["add_api"]["selected_group"] == "default":
                        results["remove"] = "ERROR : Cant remove default group"
                    else :
                        self.sql("UPDATE phone_book set group_='default'")
                        self.sql("DELETE FROM groups_ WHERE group_='{}'".format(form_dic["add_api"]["selected_group"]) )
                        results["remove"]="Group Removed"
                elif form_dic["add_api"]["remove_option"] == "opt2":
                    if form_dic["add_api"]["selected_group"] == "default":
                        results["remove"] = "ERROR : Cant remove default group"
                    else:
                        self.sql("UPDATE phone_book SET group_='{}' WHERE group_='{}'".format(form_dic["add_api"]["selected_group_to"] , form_dic["add_api"]["selected_group"] ))
                        self.sql("DELETE FROM groups_ WHERE group_='{}'".format(form_dic["add_api"]["selected_group"]) )
                    results["remove"]="Group Removed and contacts moved to other group"
                elif form_dic["add_api"]["remove_option"] == "opt3":
                    if form_dic["add_api"]["selected_group"] == "default":
                        results["remove"] = "ERROR : Cant remove default group"
                    elif form_dic["remove_move_to_new"].casefold() == "default": #for case insensitve
                        if self.sql("SELECT * from groups_ where group_ = '%s'"%form_dic["remove_move_to_new"] ) :
                            results["remove"] = "ERROR : Duplicated Group"
                    else :
                        self.sql("INSERT INTO groups_ VALUES ('%s')"%form_dic["remove_move_to_new"])
                        self.sql("UPDATE phone_book SET group_='{}' WHERE group_='{}'".format(form_dic["remove_move_to_new"] , form_dic["add_api"]["selected_group"] ))
                        self.sql("DELETE FROM groups_ WHERE group_='{}'".format(form_dic["add_api"]["selected_group"]) )
                        results["remove"]="Group Removed and contacts moved to other group"
                elif form_dic["add_api"]["remove_option"] == "opt4":
                    if form_dic["add_api"]["selected_group"] == "default":
                        results["remove"] = "ERROR : Cant remove default group"
                    else:
                        self.sql("DELETE FROM phone_book WHERE group_ ='{}'".format( form_dic["add_api"]["selected_group"]) )
                        self.sql("DELETE FROM groups_ WHERE group_='{}'".format(form_dic["add_api"]["selected_group"]) )
                        results["remove"]="Group and contacts are Removed "
            return results
        elif request_json: # sent by ajax
            ajax_dic = request_json
            results["summary"]= self.edit_groups(ajax_dic["selected_group"]) # data for summary table
            return results

    def other_database(self , database_file , statment ,fetch=False):
        with sqlite3.connect(database_file) as conn:
            cur = conn.cursor()
            if statment == "create":
                    cur.execute("""
                    CREATE TABLE IF NOT EXISTS history (
                      id integer primary key autoincrement ,
                      status text  ,
                      date_time text);
                    """)
                    conn.commit()
            else :
                cur.execute(statment)
                if fetch :
                    data = cur.fetchall()
                    conn.commit()
                    return data
                else :
                    conn.commit()

    def get_date_time (self):
        'get current date and time and reformate it , return string'
        date_time =str(datetime.datetime.now())[:16]
        day = date_time[8:10]
        month = date_time[5:7]
        year = date_time[0:4]
        time =date_time[11:]
        return day +"/"+ month +"/"+ year +" -- "+ time

    def backup (self):
        'copy current database file to backup folder [overwrite the old one]'
        os.chdir(os.getcwd())
        shutil.copy("database/phone_app_db.db" , "database/backups/phone_app_db.db")
        date_time = self.get_date_time()
        self.other_database("database/history.db", "INSERT INTO history ('status', 'date_time')VALUES ('Backup','%s')"%date_time)
        return {"last_info":date_time ,"table":self.history_update_html()}

    def restore (self):
        'copy backuped database file to database folder [overwrite the old one]'
        os.chdir(os.getcwd())
        shutil.copy("database/backups/phone_app_db.db" , "database/phone_app_db.db")
        date_time = self.get_date_time()
        self.other_database("database/history.db", "INSERT INTO history ('status', 'date_time')VALUES ('Restore','%s')"%date_time)
        return {"last_info":date_time ,"table":self.history_update_html()}


    def last_backup_restore (self):
        backup_ = self.other_database("database/history.db", "SELECT status , date_time FROM history where status ='Backup' ORDER BY id DESC limit 1 ", True)
        restore_ = self.other_database("database/history.db", "SELECT status , date_time FROM history where status ='Restore' ORDER BY id DESC limit 1 ", True)
        if backup_ :
            backup = backup_
        else :
            backup =  [[]] #nested  empty list to be same pattern on normel case , like (item [0][0][1])
        if restore_:
            restore = restore_
        else :
            restore = [[]]
        return (backup , restore)

    def history_update (self): # for render
        return self.other_database("database/history.db", "SELECT status , date_time FROM history ORDER BY id DESC", True)

    def history_update_html (self):# for ajax
        table = self.other_database("database/history.db", "SELECT status , date_time FROM history ORDER BY id DESC", True)
        html=""
        for i in table :
            html +="<tr>"
            for cells in i :
                html +="<td>"+str(cells)+"</td>"
            html+="</tr>"
        return html

class api (database) :
    'api class has method deal with ajax'
    def __init__ (self,db_file):
        'init function'
        super().__init__(db_file)

    def show_row_to_edit (self,api):
        "query specific row and send each cell in it to api to put it in edit form "
        group_list = self.query_statment("select * from groups_" )
        groups=[]
        for i in group_list :
            groups.append(i[0])
        api["group_list"]=groups
        res = self.query_statment("select * from phone_book where id = "+api["id"])
        api["name"]=res[0][1]
        api["nickname"]=res[0][2]
        api["phone_number"]=res[0][3]
        api["address"]=res[0][4]
        api["work"]=res[0][5]
        api["email"]=res[0][6]
        api["notes"]=res[0][7]
        api["group"]=res[0][8]
        return api

    def filter (self,api):
        "filter query as a table rows as html element , then put this html in api[html] "
        res = self.query_statment("select * from phone_book where "+ api["filter_by"]+" like \'%" +api["filter"]+"%\'")
        html="""
        <thead>
            <td>Name</td>
            <td>Nickname</td>
            <td>Phone Number</td>
            <td>Address</td>
            <td>Work</td>
            <td>Email</td>
            <td>Notes</td>
            <td>Group</td>
        </thead>
        """
        for rows in res :
            html+="<tr>"
            for cells in rows[1:] :
                html+= "<td id='"+str(rows[0])+"'>" + str(cells) + "</td>"
            html+="</td>"
        api["html"] = html
        return api

    def delete_type (self,api):
        "change table in 'delete page' depend on mark button case"
        res = self.query_statment("select * from phone_book where "+ api["filter_by"]+" like \'%" +api["filter"]+"%\'")
        html="""
        <thead>
            <td>Name</td>
            <td>Nickname</td>
            <td>Phone Number</td>
            <td>Address</td>
            <td>Work</td>
            <td>Email</td>
            <td>Notes</td>
            <td>Group</td>
            <td>Mark</td>
        </thead>
        """
        for rows in res :
            html+="<tr name='rows' id='"+str(rows[0])+"'>"
            for cells in rows[1:] :
                html+= "<td id='"+str(rows[0])+"'>" + str(cells) + "</td>"
            if api["case"]=="one_by_one":
                html+="</td><td><button name='delete_row' id = '"+str(rows[0])+"'>Delete</button></td>"
            elif api["case"]== "mark":
                html+="</td><td><input type='checkbox' name='checkbox_row' id = '"+str(rows[0])+"'></td>"
            elif api["case"]=="delete_alL":
                api["html"]=="ALL DELETED"
            else :
                html+="</td><td><button name='delete_row' id = '"+str(rows[0])+"'>Delete</button></td>"

        api["html"] = html
        return api
    def delete_action (self,api):
        if api["case"] == "delete_one":
            self.sql("DELETE FROM phone_book WHERE id = "+api["selected_id"][0])
            print ("DONE")
            api["case"]="one_by_one"
            api["response"]="Record Deleted - OK"
            return self.delete_type(api)
        elif api["case"] == "marked_row":
            for i in api["selected_id"]:
                self.sql("DELETE FROM phone_book WHERE id = "+str(i))
                api["case"]="mark"
                api["response"]="Record Deleted - OK"
            return self.delete_type(api)
        elif api["case"]=="delete_all" :
            self.sql("DELETE FROM phone_book")
            return self.delete_type(api)

def allowed_file(filename,allowed_extenstions):
    'check extenstions'
    last_dot_index=0
    for index , i in enumerate(filename) :
        if i =="." : last_dot_index = index
    extenstion = filename[last_dot_index+1:].lower()
    return  extenstion in allowed_extenstions

def import_file (db_object):
    'replace old database file with imported file'
    with sqlite3.connect("uploads/testing.db") as conn:
        cur = conn.cursor()
        try :
            cur.execute("SELECT groups_.group_, phone_book.name , phone_book.nickname , phone_book.phone_number , phone_book.address , phone_book.work , phone_book.notes , phone_book.email , phone_book.group_  from phone_book  , groups_")
            shutil.copy("uploads/testing.db", "database/phone_app_db.db")
            db_object.other_database("database/history.db", "INSERT INTO history (status , date_time) Values ('Import' ,'{}')".format(db_object.get_date_time()) , True )
            return True
        except : return False

def export_file (export_as ):
    db=database("database/history.db")
    db.sql( "INSERT INTO history (status , date_time) Values ('Export' ,'{}')".format(db.get_date_time()) )
    if export_as == "SQLite3.db":
        return "database/phone_app_db.db"
    elif export_as == "CSV" :
        with  sqlite3.connect("database/phone_app_db.db") as conn :
            query = conn.cursor().execute("select * from phone_book")
            with open ("files/csv_db.csv" ,"wb") as f :
                f.write("id,name,nickname,phone_number,address,work,email,notes,group\n".encode())
                for row in query :
                    f.write( (",".join([str(i).replace(",","-") for i in row])+"\n").encode() )
        return "files/csv_db.csv"

    elif export_as == "SQL" :
        with sqlite3.connect("database/phone_app_db.db") as conn:
            with open ("files/db.sql" , "w") as f :
                for line in conn.iterdump():
                    f.write('%s\n'%line)
        return "files/db.sql"
    elif export_as == "HTML" :
        data = database("database/phone_app_db.db").query_statment("SELECT * FROM phone_book")
        html="""
        <html>
        <style>
        *{
        border:1px solid black;
        }
        </style>
        <table style='width:100%'>
            <tr>
                <td>ID</td>
                <td>Name</td>
                <td>NickName</td>
                <td>Phone</td>
                <td>Address</td>
                <td>Work</td>
                <td>Email</td>
                <td>Notes</td>
                <td>Group</td>
            </tr>
        """
        for i in data :
            html+="<tr>"
            for cell in i :
                html+="<td>"+str(cell)+"</td>"
            html+=""
        html+="</table></html>"
        with open ("files/export_html.html","w") as f :
            f.write(html)
        return "files/export_html.html"


def last_export (db_object):
    try :
        return db_object.other_database("database/history.db", "SELECT date_time from history where status ='Export' order by id DESC limit 1" , True ) [0][0]
    except :
        return ""

def last_import(db_object):
    try :
        return db_object.other_database("database/history.db", "SELECT date_time from history where status ='Import' order by id DESC limit 1" , True ) [0][0]

    except :
        return ""

### END OF FILE ###
