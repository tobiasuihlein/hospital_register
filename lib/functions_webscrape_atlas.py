import pandas as pd
import requests
from bs4 import BeautifulSoup

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

def get_departments(df, soup, hospital_id):
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
    # extract data from soup
    result_list = soup.find(name='ul', class_='rte_ul')
    result_list_elements = result_list.find_all('li')

    # store departments and number of treatments in a list
    departments = {}
    for li in result_list_elements:
        try:
            department = str(li.text.split(':')[0])
            n_treatments = int(li.text.split(':')[1].strip().replace('.', ''))
            departments.update({f"{department}": n_treatments})
        except ValueError:
            department = str(li.text.split(':')[0])
            departments.update({f"{department.replace('\n', ' ').strip()}": 0})
    
    for department, n_treatments in departments.items():
        df.loc[df['hospital_id'] == hospital_id, department]= n_treatments
    
    return df

def get_details(df, soup, hospital_id):
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
    # extract data from soup
    result_list = soup.find_all(name='div', class_='c-tacho-text__text')

    # extract total treatment count
    treatment_count_number = int(result_list[0].contents[1].text.replace('.',''))
    treatment_count_description = result_list[0].contents[2].text.replace('\n','').strip().replace('(','').replace(')','')
    
    # extract nursing staff quotient
    nursing_staff_quotient_number = float(result_list[1].contents[1].text.replace(',','.'))
    nursing_staff_quotient_description = result_list[1].contents[2].text.replace('\n','').strip().replace('(','').replace(')','')

    # extract provider type
    provider_type = soup.find(name='li', class_='col-2 row-1').contents[2].text.replace('\n','').strip()

    df.loc[df['hospital_id'] == hospital_id, 'total_treatment_count_number'] = treatment_count_number
    df.loc[df['hospital_id'] == hospital_id, 'total_treatment_count_description'] = treatment_count_description
    df.loc[df['hospital_id'] == hospital_id, 'nursing_staff_quotient_number'] = nursing_staff_quotient_number
    df.loc[df['hospital_id'] == hospital_id, 'nursing_staff_quotient_description'] = nursing_staff_quotient_description
    df.loc[df['hospital_id'] == hospital_id, 'provider_type'] = provider_type

    return df