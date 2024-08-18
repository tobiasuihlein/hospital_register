print("Loading libraries")
import pandas as pd
import mysql.connector
from dotenv import load_dotenv
import os


# Load the data
print("Loading the data")

federal_states = pd.read_csv('../data/db_csv/federal_states.csv', encoding='utf-8')
federal_states = federal_states.copy()[['federal_state_code', 'federal_state_name', 'area', 'population']]

hospital_locations_df = pd.read_csv('../data/db_csv/hospital_locations.csv', encoding='utf-8', dtype={'hospital_id': str, 'zip': str})
hospital_locations_df = hospital_locations_df.copy()[['hospital_id', 'name', 'street', 'city', 'zip', 'federal_state_code', 'phone', 'mail', 'latitude', 'longitude', 'link']]

departments_dict_df = pd.read_csv('../data/db_csv/departments_dict.csv', encoding='utf-8', dtype={'department_id': str})
departments_dict_df = departments_dict_df.copy()[['department_id', 'department_name']]

hospital_departments_df = pd.read_csv('../data/db_csv/hospital_departments.csv', encoding='utf-8', dtype={'department_id': str})
hospital_departments_df = hospital_departments_df.copy()[['hospital_id', 'department_id', 'treatment_count']]

hospital_details_df = pd.read_csv('../data/db_csv/hospital_details.csv', encoding='utf-8')
hospital_details_df = hospital_details_df.copy()[['hospital_id', 'total_treatments', 'nursing_quotient', 'nursing_count', 'provider_type', 'bed_count', 'semi_residential_count', 'has_emergency_service', 'emergency_service_level']]

treatments_dict_df = pd.read_csv('../data/db_csv/treatments_dict.csv', encoding='utf-8', dtype={'treatment_id': str})
treatments_dict_df = treatments_dict_df.copy()[['treatment_code', 'treatment_name']]

hospital_treatments_df = pd.read_csv('../data/db_csv/hospital_treatments.csv', encoding='utf-8', dtype={'treatment_code': str})
hospital_treatments_df = hospital_treatments_df.copy()[['hospital_id', 'treatment_code', 'treatment_count']]

places_df = pd.read_csv('../data/db_csv/places.csv', encoding='utf-8', dtype={'zip': str})
places_df = places_df.copy()[['name', 'city_district', 'rural_district', 'zip', 'federal_state_code', 'latitude', 'longitude']]


# Connect to the database
print("Connecting to database")

load_dotenv()
DB_PW = os.getenv('DB_PW')

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password=DB_PW,
    database='hospital_register'
)


# Create cursor and insert data
cursor = connection.cursor()


# federal_states
print("Inserting federal states data")
insert_query_federal_states = """
INSERT INTO federal_states (federal_state_code, federal_state_name, area, population)
VALUES (%s, %s, %s, %s)
"""

for index, row in federal_states.iterrows():
    cursor.execute(insert_query_federal_states, (row['federal_state_code'], row['federal_state_name'], row['area'], row['population']))


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
INSERT INTO departments_dict (department_id, department_name)
VALUES (%s, %s)
"""

for index, row in departments_dict_df.iterrows():
    cursor.execute(insert_query_departments_dict, (row['department_id'], row['department_name']))


# hospital_departments
print("Inserting departments data")
insert_query_departments = """
INSERT INTO hospital_departments (hospital_id, department_id, treatment_count)
VALUES (%s, %s, %s)
""" 

for index, row in hospital_departments_df.iterrows():
    cursor.execute(insert_query_departments, (row['hospital_id'], row['department_id'], row['treatment_count']))


# treatments_dict
print("Inserting treatments dictionary data")
insert_query_treatments_dict = """
INSERT INTO treatments_dict (treatment_code, treatment_name)
VALUES (%s, %s)
"""

for index, row in treatments_dict_df.iterrows():
    cursor.execute(insert_query_treatments_dict, (row['treatment_code'], row['treatment_name']))


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
INSERT INTO hospital_details (hospital_id, total_treatments, nursing_quotient, nursing_count, provider_type, bed_count, semi_residential_count, has_emergency_service, emergency_service_level)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for index, row in hospital_details_df.iterrows():
    cursor.execute(insert_query_details, (row['hospital_id'], row['total_treatments'], row['nursing_quotient'], row['nursing_count'], row['provider_type'], row['bed_count'], row['semi_residential_count'], row['has_emergency_service'], row['emergency_service_level']))


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

