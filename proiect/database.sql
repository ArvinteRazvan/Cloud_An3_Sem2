/* first drop test tables from previous session so we have a clean database */
/* DROP SCHEMA public cascade; http://stackoverflow.com/a/13823560/1148249 */
CREATE SCHEMA IF NOT EXISTS public;
/* DROP DATABASE IF EXISTS test; */
/* CREATE DATABASE test; */
/* create the siteusers table */
CREATE TABLE IF NOT EXISTS siteusers (
  id SERIAL PRIMARY KEY,
  username VARCHAR(100) UNIQUE NOT NULL,
  password VARCHAR(60) NOT NULL,
  IT decimal(5,2) check (IT between 0 and 1),
  business decimal(5,2) check (IT between 0 and 1),
  travel decimal(5,2) check (IT between 0 and 1),
  relax decimal(5,2) check (IT between 0 and 1),
  path VARCHAR(256) NOT NULL
);
/* insert a person into the siteusers table if it does not already exist */
/* http://stackoverflow.com/questions/4069718/postgres-insert-if-does-not-exist-already */
INSERT INTO siteusers ( username, password, IT, business, travel, relax, path)
  SELECT username, password, IT, business, travel, relax, path FROM siteusers
  UNION
  VALUES (
    'admin',
    'Admin1',
	0.50,
	0.50,
	0.50,
	0.50,
	'lol'
  )
  EXCEPT
  SELECT username, password, IT, business, travel, relax, path FROM siteusers;
/* sessions */
CREATE TABLE IF NOT EXISTS sessions (
  session_id VARCHAR(36),
  person_id INTEGER NOT NULL REFERENCES siteusers (id),
  start_timestamp INTEGER DEFAULT EXTRACT(EPOCH FROM CURRENT_TIMESTAMP),
  end_timestamp INTEGER DEFAULT null
);
INSERT INTO sessions (session_id, person_id)
VALUES (
  '525be54a-1101-46bf-97d7-2e9c89dd1b16',
  '1'
);