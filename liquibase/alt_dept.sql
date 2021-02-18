--liquibase formatted sql
--changeset 1:suddha

ALTER TABLE DEPARTMENTS ADD (newColumnFlag VARCHAR (1) NOT NULL);
