DROP DATABASE IF EXISTS hospital_register;

CREATE DATABASE IF NOT EXISTS hospital_register
	CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE hospital_register;

CREATE TABLE departments_dict(
	department_id CHAR(4) PRIMARY KEY,
    department_name VARCHAR(255)
    );
    
CREATE TABLE treatments_dict(
	treatment_code VARCHAR(7) PRIMARY KEY,
    treatment_name VARCHAR(255)
    );
    
CREATE TABLE federal_states(
	federal_state_code CHAR(2) PRIMARY KEY,
    federal_state_name VARCHAR(255),
    area DECIMAL(7,2),
    population INT
    );

CREATE TABLE hospital_locations(
	hospital_id CHAR(6) PRIMARY KEY,
    name VARCHAR(255),
    street VARCHAR(255),
    city VARCHAR(255),
    zip CHAR(5),
    federal_state_code CHAR(2),
    phone VARCHAR(255),
    mail VARCHAR(255),
    beds_number INT,
    latitude DECIMAL(14, 12),
    longitude DECIMAL(15, 12),
    link VARCHAR(255),
    FOREIGN KEY (federal_state_code) REFERENCES federal_states(federal_state_code)
    );
    
CREATE TABLE hospital_departments(
	hospital_id CHAR(6),
    department_id CHAR(4),
    treatment_count INT,
    FOREIGN KEY (hospital_id) REFERENCES hospital_locations(hospital_id),
    FOREIGN KEY (department_id) REFERENCES departments_dict(department_id)
    );
  
CREATE TABLE hospital_details(
	hospital_id CHAR(6),
    total_treatments INT,
    nursing_quotient DECIMAL(5,2),
    nursing_count INT,
    provider_type VARCHAR(255),
    bed_count INT,
    semi_residential_count INT,
    has_emergency_service BOOLEAN,
    emergency_service_level INT,
    FOREIGN KEY (hospital_id) REFERENCES hospital_locations(hospital_id)
    );
    
CREATE TABLE hospital_treatments(
	hospital_id CHAR(6),
    treatment_code VARCHAR(7),
    treatment_count INT,
    FOREIGN KEY (hospital_id) REFERENCES hospital_locations(hospital_id),
    FOREIGN KEY (treatment_code) REFERENCES treatments_dict(treatment_code)
	);

CREATE TABLE hospital_certifiactes(
	hospital_id CHAR(6),
    certificate VARCHAR(255),
    FOREIGN KEY (hospital_id) REFERENCES hospital_locations(hospital_id)
    );

CREATE TABLE places(
	name VARCHAR(255),
    city_district VARCHAR(255),
    rural_district VARCHAR(255),
    zip CHAR(5),
    federal_state_code CHAR(2),
    latitude DECIMAL(8, 6),
    longitude DECIMAL(9, 6),
    FOREIGN KEY (federal_state_code) REFERENCES federal_states(federal_state_code)
	);