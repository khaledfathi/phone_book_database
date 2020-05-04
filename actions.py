#main Actions lib
import sqlite3

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

    def update_record (self,request_form_get): ############################
        'new update in tables'
        data_label =["name","nickname","phone_number","address","work","email","notes","group","new_group_flag","id_value"]
        data_values = [request_form_get(i) for i in data_label]
        data_dic={}
        for key , i in enumerate(data_values) :
            data_dic[ data_label[key] ]=i.strip()

        print (data_dic)#THIS LINE FOR TESTING ONLY

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
        with open("templates/include.html","w") as f :
            f.write(html)
        return True

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
