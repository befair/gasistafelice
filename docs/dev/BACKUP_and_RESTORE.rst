
Backup and restore procedure
============================

Since everything is stored on a RDBMS the simplest steps to backup and restore an installation are:

  1. dump database of a deployed installation: `pg_dump -U postgres $dbname > gf_dump.sql`;
  2. create database and roles in a new installation: `extras/wipe_postgres_db.sh`;
  3. restore database in the new installation: `psql -U postgres $newdbname <  gf_dump.sql`.
  
