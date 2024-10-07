CREATE DATABASE IF NOT EXISTS django_internal_db;
CREATE DATABASE IF NOT EXISTS hospital_register_db;

GRANT ALL ON django_internal_db.* TO 'hospital_user'@'%';
GRANT ALL ON hospital_register_db.* TO 'hospital_user'@'%';

FLUSH PRIVILEGES;
