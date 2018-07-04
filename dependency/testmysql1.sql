create database testdb1;
use testdb1;
create table users(
		user_id int not null auto_increment,
		user_name varchar(64) not null,
		user_pass varchar(64) not null,
		role int not null default 1 ,
		primary key (user_id),
		unique(user_name)
		);

drop table if exists accessories;
create table accessories(
        acces_id int not null auto_increment,
        param_num int not null,
        param_acces varchar(256) not null,
        primary key (acces_id)
);

drop table if EXISTS oprs;
drop table if exists materials;
create table materials(
		material_id int not null auto_increment,
		material_name varchar(64) not null,
		countnum int not null,
		reworknum int not null default 0,
		buynum int not null default 0,
		acces_id int not null default 0,
		primary key (material_id),
		unique(material_name)
		);
create table oprs(
		opr_id int not null auto_increment,
		user_id int not null,
		material_id int not null,
		diff int not null,
		oprtype varchar(16) not null,
		ismain tinyint(1) not null,
		momentary datetime not null default current_timestamp,
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
insert into materials(material_name,countnum) values('apple1',20);
insert into materials(material_name,countnum) values('orange1',30);
insert into materials(material_name,countnum) values('banana1',25);
insert into materials(material_name,countnum) values('strawberry1',35);
insert into materials(material_name,countnum) values('apple2',20);
insert into materials(material_name,countnum) values('orange2',30);
insert into materials(material_name,countnum) values('banana2',25);
insert into materials(material_name,countnum) values('strawberry2',35);
insert into materials(material_name,countnum) values('apple3',20);
insert into materials(material_name,countnum) values('orange3',30);
insert into materials(material_name,countnum) values('banana3',25);
insert into materials(material_name,countnum) values('strawberry3',35);

insert into oprs(user_id,material_id,diff,oprtype) values (2,1,20,"INITADD");
insert into oprs(user_id,material_id,diff,oprtype) values (1,3,25,"INITADD");
insert into oprs(user_id,material_id,diff,oprtype) values (3,4,35,"INITADD");
insert into oprs(user_id,material_id,diff,oprtype) values (2,2,30,"INITADD");

insert into oprs(user_id,material_id,diff,oprtype) values (2,1,20,"INITADD");
insert into oprs(user_id,material_id,diff,oprtype) values (1,3,25,"INITADD");
insert into oprs(user_id,material_id,diff,oprtype) values (3,4,35,"INITADD");
insert into oprs(user_id,material_id,diff,oprtype) values (2,2,30,"INITADD");
insert into oprs(user_id,material_id,diff,oprtype) values (2,1,20,"INITADD");
insert into oprs(user_id,material_id,diff,oprtype) values (1,3,25,"INITADD");
insert into oprs(user_id,material_id,diff,oprtype) values (3,4,35,"INITADD");
insert into oprs(user_id,material_id,diff,oprtype) values (2,2,30,"INITADD");
insert into oprs(user_id,material_id,diff,oprtype) values (2,1,20,"INITADD");
insert into oprs(user_id,material_id,diff,oprtype) values (1,3,25,"INITADD");
insert into oprs(user_id,material_id,diff,oprtype) values (3,4,35,"INITADD");
insert into oprs(user_id,material_id,diff,oprtype) values (2,2,30,"INITADD");
