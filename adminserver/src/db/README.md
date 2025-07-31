REATE ROLE local_admin WITH LOGIN PASSWORD '<in one password>';
ALTER ROLE local_admin CREATEDB;

postgres=# \du
                                    List of roles
  Role name  |                         Attributes                         | Member of 
-------------+------------------------------------------------------------+-----------
 ajwilson    | Superuser, Create role, Create DB, Replication, Bypass RLS | {}
 local_admin | Create DB                                                  | {}

---new shell---
psql postgres -U local_admin
postgres=> CREATE DATABASE adminserver;
CREATE DATABASE
postgres=> \l
                               List of databases
    Name     |    Owner    | Encoding | Collate | Ctype |   Access privileges   
-------------+-------------+----------+---------+-------+-----------------------
 adminserver | local_admin | UTF8     | C       | C     | 
 postgres    | ajwilson    | UTF8     | C       | C     | 
 template0   | ajwilson    | UTF8     | C       | C     | =c/ajwilson          +
             |             |          |         |       | ajwilson=CTc/ajwilson
 template1   | ajwilson    | UTF8     | C       | C     | =c/ajwilson          +
             |             |          |         |       | ajwilson=CTc/ajwilson
(4 rows)

