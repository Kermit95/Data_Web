drop database if exists `data_project`;
create database `data_project` default character set utf8;

grant all privileges on data_project.* to 'kermit'@'localhost' identified by '1234qwer';
flush privileges;
