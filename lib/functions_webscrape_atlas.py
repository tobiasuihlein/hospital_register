import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

def load_hospital_site(hospital_id):
    """
    Summary:
        Retrieve website content for a defined hospital from bundes-klinik-atlas.de

    Arguments:
        hospital_id (str): hospital id as used on bundes-klinik-atlas.de

    Returns:
        soup (soup): website content
    """

    request_url = f'https://bundes-klinik-atlas.de/krankenhaussuche/krankenhaus/{hospital_id}'
    response = requests.get(request_url)
    soup = BeautifulSoup(response.content, "html.parser")

    return soup


def get_departments(soup, hospital_id):
    """
    Summary:
        Extact department designations and respective numbers of treatments for a defined hospital from website content and store them in a pandas DataFrame

    Arguments:
        df (pd.DataFrame): DataFrame to store the data in
        soup (soup): website content
        hospital_id (str): hospital id as used on bundes-klinik-atlas.de

    Returns:
        df (pd.DataFrame): DataFrame with the extracted data
    """
    # initialize empty lists to store the extracted data
    hospital_ids = []
    department_names = []
    department_counts = []
    # extract data from soup
    result_list = soup.find(name='ul', class_='rte_ul')
    try:
        result_list_elements = result_list.find_all('li')
        # store departments and number of treatments in a list
        for li in result_list_elements:
            try:
                department_name = str(li.text.split(':')[0])
                department_count = int(li.text.split(':')[1].strip().replace('.', ''))
            except ValueError:
                department_name = str(li.text.split(':')[0]).replace('\n', ' ').strip()
                department_count = 0

            hospital_ids.append(hospital_id)
            department_names.append(department_name)
            department_counts.append(department_count)
    except AttributeError:
        print('No departments found')
    return hospital_ids, department_names, department_counts


def get_details(soup, hospital_id):
    """
    Summary:
        Extact details for a defined hospital from website content and store them in a pandas DataFrame

    Arguments:
        df (pd.DataFrame): DataFrame to store the data in
        soup (soup): website content
        hospital_id (str): hospital id as used on bundes-klinik-atlas.de

    Returns:
        df (pd.DataFrame): DataFrame with the extracted data
    """
    # extract data from soup for treatment count and nursing staff quotient
    result_list = soup.find_all(name='div', class_='c-tacho-text__text')

    # extract total treatment count
    try:
        total_treatments_count = int(result_list[0].contents[1].text.replace('.',''))
        total_treatments_label = result_list[0].contents[2].text.replace('\n','').strip().replace('(','').replace(')','')
    except ValueError:
        total_treatments_count = 0
        total_treatments_label = 'sehr wenige'
    
    # extract nursing staff quotient
    nursing_quotient_count = float(result_list[1].contents[1].text.replace(',','.'))
    nursing_quotient_label = result_list[1].contents[2].text.replace('\n','').strip().replace('(','').replace(')','')

    # extract nursing count
    nursing_count = soup.find_all(name='div', class_='ce-accordion__header__components')[1].find_all(name='strong')[1].text.strip()

    # extract provider type
    provider_type = soup.find(name='li', class_='col-2 row-1').contents[2].text.replace('\n','').strip()

    # extrect treatment slots
    bed_count = soup.find(name='li', class_='col-2 row-2 row-span-2 location-size').find(name='small').text.split('(')[0].split(':')[1].strip().split(' ')[0]
    try:
        semi_residential_count = soup.find(name='li', class_='col-2 row-2 row-span-2 location-size').find(name='small').text.split('(')[1].split(':')[1].split('\n')[0].strip()
    except IndexError:
        semi_residential_count = 0

    # extract emergency service info
    emergency_service = soup.find_all(name='div', class_='ce-accordion__header__components')[-1].find_all(name='strong')[0].text.strip()

    return hospital_id, total_treatments_count, total_treatments_label, nursing_quotient_count, nursing_quotient_label, nursing_count, provider_type, bed_count, semi_residential_count, emergency_service


def get_treatments(hospital_ids, treatments_dictionary):
    # initialize empty lists to store the extracted data
    list_for_df_hospital_id = []
    list_for_df_treatment_code = []
    list_for_df_count_number = []
    list_for_df_count_label = []
    # loop through all hospitals and treatments
    for hospital_id in hospital_ids:
        print(f'Processing hospital with ID {hospital_id}')
        for treatment_key, treatment_value in treatments_dictionary.items():
            treatment_code = treatment_value['code']
            treatment_searchlabel = treatment_value['searchlabel']
            treatment_cHash = treatment_value['cHash']
            # GET method
            request_url = f'https://bundes-klinik-atlas.de/krankenhaussuche/krankenhaus/{hospital_id}/?tx_tverzhospitaldata_show%5Bquantile%5D=114%2C202%2C253%2C343&tx_tverzhospitaldata_show%5Bsearchlabel%5D={treatment_searchlabel}&tx_tverzhospitaldata_show%5Bsimplesearch%5D=1&tx_tverzhospitaldata_show%5Btreatmentcode%5D={treatment_code}&cHash={treatment_cHash}'
            response = requests.get(request_url)

            # parse HTML
            soup = BeautifulSoup(response.content, "html.parser")

            # extract data
            result_list = soup.find_all(name='div', class_='c-tacho-text__text')

            # extract treatment count
            try:
                treatment_count_number = int(result_list[0].contents[1].text.replace('.',''))
                treatment_count_label = result_list[0].contents[2].text.replace('(','').replace(')','').strip()
            except ValueError:
                treatment_count_number = 0
                treatment_count_label = 'sehr wenige'

            # store data in lists
            list_for_df_hospital_id.append(hospital_id)
            list_for_df_treatment_code.append(treatment_code)
            list_for_df_count_number.append(treatment_count_number)
            list_for_df_count_label.append(treatment_count_label)
            
            time.sleep(15) # wait 15 seconds before next request
    return list_for_df_hospital_id, list_for_df_treatment_code, list_for_df_count_number, list_for_df_count_label


def get_certificates(soup, hospital_id):
    certificates = []
    hospital_ids = []
    try:
        for certificate in soup.find_all(name='div', id='content-menu-seals-certificates')[0].find(name='ul', class_='c-checklist').find_all(name='li'):
            certificates.append(certificate.text)
            hospital_ids.append(hospital_id)
        return hospital_ids, certificates
    except:
        print('no certificates found')

    return hospital_ids, certificates