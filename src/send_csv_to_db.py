import pandas as pd
import mysql.connector
from dotenv import load_dotenv
import os


load_dotenv()
DB_PW = os.getenv('DB_PW')


# Load the data
print("Loading the data")

hospital_locations_df = pd.read_csv('../data/db_csv/hospital_locations.csv', encoding='utf-8')
hospital_locations_df = hospital_locations_df.copy()[['hospital_id', 'name', 'street', 'city', 'zip', 'phone', 'mail', 'beds_number', 'latitude', 'longitude', 'link']]
print(hospital_locations_df.columns)

hospital_departments_dict_df = pd.read_csv('../data/db_csv/hospital_departments_dict.csv', encoding='utf-8', dtype={'department_id': str})
hospital_departments_dict_df = hospital_departments_dict_df.copy()[['department_id', 'department_label']]

hospital_departments_df = pd.read_csv('../data/db_csv/hospital_departments.csv', encoding='utf-8', dtype={'department_id': str})
hospital_departments_df = hospital_departments_df.copy()[['hospital_id', 'department_id', 'treatment_count']]


# Connect to the database
print("Connecting to database")
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password=DB_PW,
    database='hospital_register'
)


# Insert data
cursor = connection.cursor()

# hospital_locations
print("Inserting locations data")
insert_query_locations = """
INSERT INTO hospital_locations (hospital_id, name, street, city, zip, phone, mail, beds_number, latitude, longitude, link)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for index, row in hospital_locations_df.iterrows():
    cursor.execute(insert_query_locations, (row['hospital_id'], row['name'], row['street'], row['city'], row['zip'], row['phone'], row['mail'], row['beds_number'], row['latitude'], row['longitude'], row['link']))

# hospital_departments_dict
print("Inserting departments dictionary data")
insert_query_departments_dict = """
INSERT INTO hospital_departments_dict (department_id, department_label)
VALUES (%s, %s)
"""

for index, row in hospital_departments_dict_df.iterrows():
    cursor.execute(insert_query_departments_dict, (row['department_id'], row['department_label']))

# hospital_departments
print("Inserting departments data")
insert_query_departments = """
INSERT INTO hospital_departments (hospital_id, department_id, treatment_count)
VALUES (%s, %s, %s)
"""

for index, row in hospital_departments_df.iterrows():
    cursor.execute(insert_query_departments, (row['hospital_id'], row['department_id'], row['treatment_count']))

connection.commit()
cursor.close()


# Close the connection
connection.close()

print('Data inserted successfully')

