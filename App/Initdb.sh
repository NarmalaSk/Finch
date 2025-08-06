sudo -i -u postgres
psql
CREATE USER finch_user WITH PASSWORD 'password';
CREATE DATABASE finch_db OWNER finch_user;
GRANT ALL PRIVILEGES ON DATABASE finch_db TO finch_user;


\q

psql -U finch_user -d finch_db -h localhost


\conninfo
\dt
