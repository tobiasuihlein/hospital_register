DROP DATABASE IF EXISTS hospital_register;

CREATE DATABASE IF NOT EXISTS hospital_register
	CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE hospital_register;

CREATE TABLE languages(
	language_code CHAR(2) PRIMARY KEY,
    language_name VARCHAR(50)
    );

CREATE TABLE provider_type_codes(
	provider_type_code CHAR(1) PRIMARY KEY
	);
    
CREATE TABLE provider_types_dict(
	provider_type_code CHAR(1),
    provider_type_name VARCHAR(50),
    language_code CHAR(2),
    FOREIGN KEY (provider_type_code) REFERENCES provider_type_codes(provider_type_code),
    FOREIGN KEY (language_code) REFERENCES languages(language_code)
    );

CREATE TABLE department_codes(
	department_code CHAR(4) PRIMARY KEY
	);

CREATE TABLE departments_dict(
	department_code CHAR(4),
    parent_department_code CHAR(4),
    department_name VARCHAR(255),
    parent_department_name VARCHAR(255),
    language_code CHAR(2),
    FOREIGN KEY (department_code) REFERENCES department_codes(department_code),
    FOREIGN KEY (language_code) REFERENCES languages(language_code)
    );
    
CREATE TABLE treatment_codes(
	treatment_code VARCHAR(7) PRIMARY KEY
	);
    
CREATE TABLE treatments_dict(
	treatment_code VARCHAR(7),
    treatment_name VARCHAR(255),
    language_code CHAR(2),
    FOREIGN KEY (treatment_code) REFERENCES treatment_codes(treatment_code),
    FOREIGN KEY (language_code) REFERENCES languages(language_code)
    );

CREATE TABLE federal_states(
	federal_state_code CHAR(2) PRIMARY KEY,
    area DECIMAL(7,2),
    population INT
    );
    
CREATE TABLE federal_states_dict(
	federal_state_code CHAR(2),
    federal_state_name VARCHAR(255),
    language_code CHAR(2),
    FOREIGN KEY (federal_state_code) REFERENCES federal_states(federal_state_code),
    FOREIGN KEY (language_code) REFERENCES languages(language_code)
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
    latitude DECIMAL(14, 12),
    longitude DECIMAL(15, 12),
    link VARCHAR(255),
    FOREIGN KEY (federal_state_code) REFERENCES federal_states(federal_state_code)
    );
    
CREATE TABLE hospital_departments(
	hospital_id CHAR(6),
    department_code CHAR(4),
    treatment_count INT,
    FOREIGN KEY (hospital_id) REFERENCES hospital_locations(hospital_id),
    FOREIGN KEY (department_code) REFERENCES department_codes(department_code)
    );
  
CREATE TABLE hospital_details(
	hospital_id CHAR(6),
    total_treatments INT,
    nursing_quotient DECIMAL(5,2),
    nursing_count INT,
    provider_type_code CHAR(1),
    bed_count INT,
    semi_residential_count INT,
    total_stations_count INT,
    has_emergency_service BOOLEAN,
    emergency_service_level INT,
    FOREIGN KEY (hospital_id) REFERENCES hospital_locations(hospital_id),
    FOREIGN KEY (provider_type_code) REFERENCES provider_type_codes(provider_type_code)
    );
    
CREATE TABLE hospital_treatments(
	hospital_id CHAR(6),
    treatment_code VARCHAR(7),
    treatment_count INT,
    FOREIGN KEY (hospital_id) REFERENCES hospital_locations(hospital_id),
    FOREIGN KEY (treatment_code) REFERENCES treatment_codes(treatment_code)
	);

CREATE TABLE hospital_certificates(
	hospital_id CHAR(6),
    certificate VARCHAR(255),
    language_code CHAR(2),
    FOREIGN KEY (hospital_id) REFERENCES hospital_locations(hospital_id),
    FOREIGN KEY (language_code) REFERENCES languages(language_code)
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