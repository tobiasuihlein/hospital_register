CREATE DATABASE IF NOT EXISTS hospital_register
	CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;


USE hospital_register;

CREATE TABLE hospital_locations(
	hospital_id CHAR(6) PRIMARY KEY,
    name VARCHAR(250),
    street VARCHAR(255),
    city VARCHAR(255),
    zip CHAR(5),
    phone VARCHAR(255),
    mail VARCHAR(255),
    beds_number INT,
    latitude DECIMAL(14, 12),
    longitude DECIMAL(15, 12),
    link VARCHAR(255)
    );
    
CREATE TABLE hospital_departments_dict(
	department_id CHAR(4) PRIMARY KEY,
    department_label VARCHAR(255)
    );
    
CREATE TABLE hospital_departments(
	hospital_id CHAR(6),
    department_id CHAR(4),
    treatment_count INT,
    FOREIGN KEY (hospital_id) REFERENCES hospital_locations(hospital_id),
    FOREIGN KEY (department_id) REFERENCES hospital_departments_dict(department_id)
    );
    
DROP TABLE hospital_departments;
DROP TABLE hospital_locations;
DROP TABLE hospital_departments_dict;