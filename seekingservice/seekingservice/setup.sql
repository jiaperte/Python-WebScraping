drop table seekingservice;


create table seekingservice (
  id         serial primary key,
  company_name       varchar(255),
  owner      varchar(255),
  cellphone       varchar(64) not null unique,
  address   varchar(255)
);

