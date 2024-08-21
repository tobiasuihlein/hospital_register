# This script sends the data from the csv files to the database

print("Loading libraries")
import pandas as pd
import mysql.connector
from dotenv import load_dotenv
import os


# Load the data
print("Loading the data")

languages = pd.DataFrame({'language_code': ['de', 'en'], 'language_name': ['German', 'English']})

provider_type_codes = pd.read_csv('../data/db_csv/provider_type_codes.csv', encoding='utf-8')
provider_type_codes = provider_type_codes.copy()[['provider_type_code']]

provider_types_dict = pd.read_csv('../data/db_csv/provider_types_dict.csv', encoding='utf-8')
provider_types_dict = provider_types_dict.copy()[['provider_type_code', 'provider_type_name', 'language_code']]

department_codes = pd.read_csv('../data/db_csv/department_codes.csv', encoding='utf-8', dtype={'department_code': str})
department_codes = department_codes.copy()[['department_code']]

treatment_codes = pd.read_csv('../data/db_csv/treatment_codes.csv', encoding='utf-8')
treatment_codes = treatment_codes.copy()[['treatment_code']]

federal_states = pd.read_csv('../data/db_csv/federal_states.csv', encoding='utf-8')
federal_states = federal_states.copy()[['federal_state_code', 'area', 'population']]

federal_states_dict = pd.read_csv('../data/db_csv/federal_states_dict.csv', encoding='utf-8')
federal_states_dict = federal_states_dict.copy()[['federal_state_code', 'federal_state_name', 'language_code']]

hospital_locations_df = pd.read_csv('../data/db_csv/hospital_locations.csv', encoding='utf-8', dtype={'hospital_id': str, 'zip': str})
hospital_locations_df = hospital_locations_df.copy()[['hospital_id', 'name', 'street', 'city', 'zip', 'federal_state_code', 'phone', 'mail', 'latitude', 'longitude', 'link']]

departments_dict_df = pd.read_csv('../data/db_csv/departments_dict.csv', encoding='utf-8', dtype={'department_code': str})
departments_dict_df = departments_dict_df.copy()[['department_code', 'parent_department_code', 'department_name', 'parent_department_name', 'language_code']]

hospital_departments_df = pd.read_csv('../data/db_csv/hospital_departments.csv', encoding='utf-8', dtype={'department_code': str})
hospital_departments_df = hospital_departments_df.copy()[['hospital_id', 'department_code', 'treatment_count']]

hospital_details_df = pd.read_csv('../data/db_csv/hospital_details.csv', encoding='utf-8')
hospital_details_df = hospital_details_df.copy()[['hospital_id', 'total_treatments', 'nursing_quotient', 'nursing_count', 'provider_type_code', 'bed_count', 'semi_residential_count', 'total_stations_count', 'has_emergency_service', 'emergency_service_level']]

treatments_dict_df = pd.read_csv('../data/db_csv/treatments_dict.csv', encoding='utf-8', dtype={'treatment_id': str})
treatments_dict_df = treatments_dict_df.copy()[['treatment_code', 'treatment_name', 'language_code']]

hospital_treatments_df = pd.read_csv('../data/db_csv/hospital_treatments.csv', encoding='utf-8', dtype={'treatment_code': str})
hospital_treatments_df = hospital_treatments_df.copy()[['hospital_id', 'treatment_code', 'treatment_count']]

hospital_certificates_df = pd.read_csv('../data/db_csv/hospital_certificates.csv', encoding='utf-8')
hospital_certificates_df = hospital_certificates_df.copy()[['hospital_id', 'certificate', 'language_code']]

places_df = pd.read_csv('../data/db_csv/places.csv', encoding='utf-8', dtype={'zip': str})
places_df = places_df.copy()[['name', 'city_district', 'rural_district', 'zip', 'federal_state_code', 'latitude', 'longitude']]


# Connect to database
print("Connecting to database")

load_dotenv()
DB_PW = os.getenv('DB_PW')

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password=DB_PW,
    database='hospital_register'
)


# Create cursor and insert data in the following
cursor = connection.cursor()

# languages
print("Inserting languages data")
insert_query_languages = """
INSERT INTO languages (language_code, language_name)
VALUES (%s, %s)
"""

for index, row in languages.iterrows():
    cursor.execute(insert_query_languages, (row['language_code'], row['language_name']))


# provider_type_codes
print("Inserting provider type codes data")
insert_query_provider_type_codes = """
INSERT INTO provider_type_codes (provider_type_code)
VALUES (%s)
"""

for index, row in provider_type_codes.iterrows():
    cursor.execute(insert_query_provider_type_codes, (row['provider_type_code'],))


# provider_types_dict
print("Inserting provider types dictionary data")
insert_query_provider_types_dict = """
INSERT INTO provider_types_dict (provider_type_code, provider_type_name, language_code)
VALUES (%s, %s, %s)
"""

for index, row in provider_types_dict.iterrows():
    cursor.execute(insert_query_provider_types_dict, (row['provider_type_code'], row['provider_type_name'], row['language_code']))


# department_codes
print("Inserting department codes data")
insert_query_department_codes = """
INSERT INTO department_codes (department_code)
VALUES (%s)
"""

for index, row in department_codes.iterrows():
    cursor.execute(insert_query_department_codes, (row['department_code'],))


# treatment_codes
print("Inserting treatment codes data")
insert_query_treatment_codes = """
INSERT INTO treatment_codes (treatment_code)
VALUES (%s)
"""

for index, row in treatment_codes.iterrows():
    cursor.execute(insert_query_treatment_codes, (row['treatment_code'],))


# federal_states
print("Inserting federal states data")
insert_query_federal_states = """
INSERT INTO federal_states (federal_state_code, area, population)
VALUES (%s, %s, %s)
"""

for index, row in federal_states.iterrows():
    cursor.execute(insert_query_federal_states, (row['federal_state_code'], row['area'], row['population']))


# federal_states_dict
print("Inserting federal states dictionary data")
insert_query_federal_states_dict = """
INSERT INTO federal_states_dict (federal_state_code, federal_state_name, language_code)
VALUES (%s, %s, %s)
"""

for index, row in federal_states_dict.iterrows():
    cursor.execute(insert_query_federal_states_dict, (row['federal_state_code'], row['federal_state_name'], row['language_code']))


# hospital_locations
print("Inserting locations data")
insert_query_locations = """
INSERT INTO hospital_locations (hospital_id, name, street, city, zip, federal_state_code, phone, mail, latitude, longitude, link)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for index, row in hospital_locations_df.iterrows():
    cursor.execute(insert_query_locations, (row['hospital_id'], row['name'], row['street'], row['city'], row['zip'], row['federal_state_code'], row['phone'], row['mail'], row['latitude'], row['longitude'], row['link']))


# departments_dict
print("Inserting departments dictionary data")
insert_query_departments_dict = """
INSERT INTO departments_dict (department_code, parent_department_code, department_name, parent_department_name, language_code)
VALUES (%s, %s, %s, %s, %s)
"""

for index, row in departments_dict_df.iterrows():
    cursor.execute(insert_query_departments_dict, (row['department_code'], row['parent_department_code'], row['department_name'], row['parent_department_name'], row['language_code']))

# hospital_departments
print("Inserting departments data")
insert_query_departments = """
INSERT INTO hospital_departments (hospital_id, department_code, treatment_count)
VALUES (%s, %s, %s)
""" 

for index, row in hospital_departments_df.iterrows():
    cursor.execute(insert_query_departments, (row['hospital_id'], row['department_code'], row['treatment_count']))


# treatments_dict
print("Inserting treatments dictionary data")
insert_query_treatments_dict = """
INSERT INTO treatments_dict (treatment_code, treatment_name, language_code)
VALUES (%s, %s, %s)
"""

for index, row in treatments_dict_df.iterrows():
    cursor.execute(insert_query_treatments_dict, (row['treatment_code'], row['treatment_name'], row['language_code']))


# hospital_treatments
print("Inserting treatments data")
insert_query_treatments = """
INSERT INTO hospital_treatments (hospital_id, treatment_code, treatment_count)
VALUES (%s, %s, %s)
"""

for index, row in hospital_treatments_df.iterrows():
    cursor.execute(insert_query_treatments, (row['hospital_id'], row['treatment_code'], row['treatment_count']))


# hospital_details
print("Inserting details data")
insert_query_details = """
INSERT INTO hospital_details (hospital_id, total_treatments, nursing_quotient, nursing_count, provider_type_code, bed_count, semi_residential_count, total_stations_count, has_emergency_service, emergency_service_level)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for index, row in hospital_details_df.iterrows():
    cursor.execute(insert_query_details, (row['hospital_id'], row['total_treatments'], row['nursing_quotient'], row['nursing_count'], row['provider_type_code'], row['bed_count'], row['semi_residential_count'], row['total_stations_count'], row['has_emergency_service'], row['emergency_service_level']))


# hospital_certificates
print("Inserting certificates data")
insert_query_certificates = """
INSERT INTO hospital_certificates (hospital_id, certificate, language_code)
VALUES (%s, %s, %s)
"""

for index, row in hospital_certificates_df.iterrows():
    cursor.execute(insert_query_certificates, (row['hospital_id'], row['certificate'], row['language_code']))

# places
print("Inserting places data")
insert_query_places = """
INSERT INTO places (name, city_district, rural_district, zip, federal_state_code, latitude, longitude)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

for index, row in places_df.iterrows():
    cursor.execute(insert_query_places, (row['name'], row['city_district'], row['rural_district'], row['zip'], row['federal_state_code'], row['latitude'], row['longitude']))


# Commit the transaction
connection.commit()
cursor.close()


# Close the connection
connection.close()


print('Data inserted successfully')

