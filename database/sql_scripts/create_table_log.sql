create table log(
    id int auto_increment primary key,
    ts timestamp default current_timestamp,
    data1 varchar(128) not null,
    data2 varchar(128) not null,
    ip varchar(128) not null,
    browser_string varchar(256),
    results varchar(128) not null
);
