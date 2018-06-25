create database testdb1;
use testdb1;
create table users(
		user_id int not null auto_increment,
		user_name varchar(64) not null,
		user_pass varchar(64) not null,
		primary key (user_id),
		unique(user_name)
		);
create table materials(
		material_id int not null auto_increment,
		material_name varchar(64) not null,
		countnum int not null,
		primary key (material_id),
		unique(material_name)
		);
create table oprs(
		opr_id int not null auto_increment,
		user_id int not null,
		material_id int not null,
		diff int not null,
--		timestamp datetime default current_timestamp,
		primary key (opr_id),
		foreign key (user_id) references users(user_id),
		foreign key (material_id) references materials(material_id)
		);

insert into users(user_name,user_pass) values('zhang','1234');
insert into users(user_name,user_pass) values('wang','1234');
insert into users(user_name,user_pass) values('zhao','1234');

insert into materials(material_name,countnum) values('apple',20);
insert into materials(material_name,countnum) values('orange',30);
insert into materials(material_name,countnum) values('banana',25);
insert into materials(material_name,countnum) values('strawberry',35);

insert into oprs(user_id,material_id,diff) values (2,1,20);
insert into oprs(user_id,material_id,diff) values (1,3,25);
insert into oprs(user_id,material_id,diff) values (3,4,35);
insert into oprs(user_id,material_id,diff) values (2,2,30);