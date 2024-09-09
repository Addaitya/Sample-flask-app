create table persons(
    id integer primary key AUTOINCREMENT ,
    name text,
    age integer,
    photo_id text unique
);

insert into persons(name, age, photo_id) values ("Aditya", 20, "a.png"), ("Aryan", 20, "b.jpg"), ("Divyansh", 20, "c.jpg"), ("Arman", 23, "d.jpg");