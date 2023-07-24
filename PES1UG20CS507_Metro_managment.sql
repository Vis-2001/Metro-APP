    -- createting tables
create table stations(station_name varchar(20) not null,sid int primary key not null);
create table fare(to_station_id int,from_station_id int,cost decimal(10,3),foreign key(to_station_id) references stations(sid),foreign key(from_station_id) references stations(sid),primary key(to_station_id,from_station_id));
create table card(cid int not null primary key,balance decimal(10,3),start_date date default curdate(),end_date date);
create table user(Uname varchar(20),biometric binary(5) primary key not null);
create table user_card(Uname varchar(20) not null,CID int not null, foreign key(CID) references card(cid),primary key(Uname,CID));
create table transaction(tid int not null primary key,cid int not null,Uname varchar(20),payment_type varchar(10),amount decimal(10,3),entry_id int,entry_time timestamp,exit_id int,exit_time time,foreign key(cid) references card(cid),foreign key(entry_id) references stations(sid),foreign key(exit_id) references stations(sid));
alter table transaction modify column entry_time timestamp default now();
alter table transaction modify column exit_time timestamp default now();

-- inserting values
 insert into stations values('National Collage',1),('Lalbagh',2),('South End Circle',3);
 insert into fare values(1,2,10),(1,3,15),(2,1,10),(2,3,10),(3,1,15),(3,2,10);
 insert into card(cid,balance) values(1234,150.0),(1243,500),(1342,75.42);
 insert into user values('Vishal','00110'),('Nitish','11111'),('Yash','11001'),('Yashas','10101');
 insert into user_card values('Vishal',1234),('Vishal',1243),('Yash',1243),('Nitish',1342),('Yashas',1342),('Yashas',1243);
 insert into transaction(tid,cid,Uname,payment_type,amount,entry_id) values(1,1234,'Vishal','cash',100,1),(4,1342,'Nitish','online',50,2);
 insert into transaction(tid,cid,Uname,payment_type,amount,entry_id,exit_id) values(2,1243,'Yashas','card',-10,2,1),(3,1243,'Vishal','card',-15,1,3);

-- triggers to set end_date for a card 
delimiter $$
create trigger exp_dat before insert on card for each row
begin
set new.end_date=new.start_date+00050000;
end $$
delimiter

select * from card

-- function no of passengers travelling on a specific day
delimiter $$
create function passen(tdate date)
returns int 
deterministic
begin 
declare ret int;
select count(*) into ret from transaction where date(entry_time)=tdate and exit_id<>0;
return ret;
end $$
delimiter

select distinct date(entry_time),passen(date(entry_time)) from transaction

-- procedure to return the no of users using a particular card
delimiter $$
create procedure card_users(in carid int)
deterministic
begin
select count(*) as users from user_card where CID=carid;
end $$
delimiter

SET @p0='1243';
CALL card_users(@p0);

-- cursor to put cards in expiry table after end_date
delimitier $$
create procedure bup()
deterministic
begin
declare done int default 0;
declare c int;
declare b decimal(10,3);
declare e date;
declare cur cursor for select cid,balance,end_date from card;
declare continue handler for not found set done=1;
open cur;
label:Loop
fetch cur into c,b,e;
if e>curdate() THEN
insert into backup values(c,e);
end if;
if done=1 then leave label;
end if;
end loop;
close cur;
end $$
delimiter;



