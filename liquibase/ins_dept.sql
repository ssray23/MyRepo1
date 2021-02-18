--liquibase formatted sql
--changeset 1:suddha

insert into DEPARTMENTS values (1, "HR", 1, "H");
insert into DEPARTMENTS values (2, "IT", 1, "I");
insert into DEPARTMENTS values (3, "Security", 1, "S");
commit;
