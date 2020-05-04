
/*Force SQLite to use foreign key*/
PRAGMA foreign_key = on;

/*Creat Group Table*/
CREATE TABLE IF NOT EXISTS groups_ (group_ text primary key);

/*Create Phone Book Table*/
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


/*Insert Main Default value that in phone book into group to avoid foreign_key error*/
INSERT INTO groups_ VALUES ('default');
