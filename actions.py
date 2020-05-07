#main Actions lib
import sqlite3 , json

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
###############################
###############################
###############################
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
        if  request_form :
            elements=["rename_field","new_group_text","remove_move_to_new","add_api"]
            for i in elements :
                form_dic[i] = request_form(i)
            form_dic["add_api"] = json.loads(form_dic["add_api"])
            results["form_dic"]=form_dic #save form data in result dictionary to use it in return
            results["summary"]= self.edit_groups(form_dic["add_api"]["selected_group"]) # data for summary table

            if form_dic["add_api"]["case"] =="rename" :
                if not form_dic["rename_field"]:
                    results["rename"] ="Nothing Changed : Empty Field"
                elif form_dic['add_api']["selected_group"] == 'default':
                    results["rename"] ="Error : You cant Edit 'default' Group"
                elif form_dic["add_api"]["case"] == "create_new":
                    #check duplication first
                    #handle error
                    #insert new group
                    results["create_new"] ="1"
                    return"DONE"
                else :
                    #self.query_statment("UPDATE phone_book SET group_='{}' WHERE group_='{}'".format(form_dic["rename_field"] , form_dic['add_api']['selected_group']))
                    results["rename"] ="Group Renamed"

                return results

            return results
        elif request_json:
            ajax_dic = request_json
            results["summary"]= self.edit_groups(ajax_dic["selected_group"]) # data for summary table
            return results






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
