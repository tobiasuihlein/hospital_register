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
    """
    Summary:
        Extact information about treatment counts for specific treatments for defined hospitals from website content and return them in lists

    Arguments:
        hospital_ids (list): list with hospital ids to be scraped

    Returns:
        list_for_df_hospital_id (list): list with hospital ids
        list_for_df_treatment_code (list): list with treatment codes
        list_for_df_count_number (list): list with treatment counts
        list_for_df_count_label (list): list with treatment count labels
    """
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
    """
    Summary:
        Extact certificate informations for a defined hospital from website content and return them in a list

    Arguments:
        soup (soup): website content
        hospital_id (str): hospital id as used on bundes-klinik-atlas.de

    Returns:
        hospital_ids (list): list with hospital ids
        certificates (list): list with certificates
    """
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

# Create dictionary with treatment names as keys and urls as values
def get_url_dict():
    """
    Summary:
        Create dictionary with treatment names as keys and urls as values
    
    Arguments:
        None
    
    Returns:
        url_dict (dict): dictionary with treatment names as keys and urls as values
        """
    url_dict ={'Chirurgischer Herzklappenersatz': 'https://bundes-klinik-atlas.de/krankenhaussuche/krankenhaus/771056/?tx_tverzhospitaldata_show%5Bquantile%5D=114%2C202%2C253%2C343&tx_tverzhospitaldata_show%5Bsearchlabel%5D=Chirurgischer%20Herzklappenersatz&tx_tverzhospitaldata_show%5Bsimplesearch%5D=1&tx_tverzhospitaldata_show%5Btreatmentcode%5D=KAHKO0&cHash=6488c3f4b1c6d9c491b41ed9e9c59a11',
            'Minimal-invasiver Herzklappenersatz': 'https://bundes-klinik-atlas.de/krankenhaussuche/krankenhaus/771056/?tx_tverzhospitaldata_show%5Bquantile%5D=114%2C202%2C253%2C343&tx_tverzhospitaldata_show%5Bsearchlabel%5D=Minimal-invasiver%20Herzklappenersatz&tx_tverzhospitaldata_show%5Bsimplesearch%5D=1&tx_tverzhospitaldata_show%5Btreatmentcode%5D=KAHM0&cHash=50c6a7f418b8bba0fd937e323b8eac77',
            'Bypassoperation des Herzens': 'https://bundes-klinik-atlas.de/krankenhaussuche/krankenhaus/771056/?tx_tverzhospitaldata_show%5Bquantile%5D=114%2C202%2C253%2C343&tx_tverzhospitaldata_show%5Bsearchlabel%5D=Bypassoperation%20des%20Herzens&tx_tverzhospitaldata_show%5Bsimplesearch%5D=1&tx_tverzhospitaldata_show%5Btreatmentcode%5D=KAKIA&cHash=d70d02d9a5fca4c88484fe1f48e71e7f',
            'Herzkatheter mit Stent': 'https://bundes-klinik-atlas.de/krankenhaussuche/krankenhaus/771056/?tx_tverzhospitaldata_show%5Bquantile%5D=114%2C202%2C253%2C343&tx_tverzhospitaldata_show%5Bsearchlabel%5D=Herzkatheter%20mit%20Stent&tx_tverzhospitaldata_show%5Bsimplesearch%5D=1&tx_tverzhospitaldata_show%5Btreatmentcode%5D=KAKIB&cHash=7cae1fe1edf884bd4a96e34171e8cdf3',
            'Lungenentzündung': 'https://bundes-klinik-atlas.de/krankenhaussuche/krankenhaus/772997/?tx_tverzhospitaldata_show%5Bquantile%5D=92%2C184%2C282%2C412&tx_tverzhospitaldata_show%5Bsearchlabel%5D=Lungenentz%C3%BCndung&tx_tverzhospitaldata_show%5Bsimplesearch%5D=1&tx_tverzhospitaldata_show%5Btreatmentcode%5D=KALE0&cHash=bcf4ebff7a7f83de638c9932e30b42dd',
            'Brustkrebs-Operation': 'https://bundes-klinik-atlas.de/krankenhaussuche/krankenhaus/772063/?tx_tverzhospitaldata_show%5Bquantile%5D=9%2C57%2C141%2C217&tx_tverzhospitaldata_show%5Bsearchlabel%5D=Brustkrebs-Operation&tx_tverzhospitaldata_show%5Bsimplesearch%5D=1&tx_tverzhospitaldata_show%5Btreatmentcode%5D=KABK0&cHash=f3404911efb4741fcfb6a70f4fd95837',
            'Lungenkrebs-Operation': 'https://bundes-klinik-atlas.de/krankenhaussuche/krankenhaus/771217/?tx_tverzhospitaldata_show%5Bquantile%5D=4%2C15%2C38%2C73&tx_tverzhospitaldata_show%5Bsearchlabel%5D=Lungenkrebs-Operation&tx_tverzhospitaldata_show%5Bsimplesearch%5D=1&tx_tverzhospitaldata_show%5Btreatmentcode%5D=KALK0&cHash=e3c44782d684bf077683b1dcff0563e8',
            'Darmkrebs-Operation': 'https://bundes-klinik-atlas.de/krankenhaussuche/krankenhaus/771374/?tx_tverzhospitaldata_show%5Bquantile%5D=17%2C30%2C47%2C72&tx_tverzhospitaldata_show%5Bsearchlabel%5D=Darmkrebs-Operation&tx_tverzhospitaldata_show%5Bsimplesearch%5D=1&tx_tverzhospitaldata_show%5Btreatmentcode%5D=KADK0&cHash=11cb4bad024311c202ffc41fafbc1d2e',
            'Speiseröhren und Magenkrebs-Operation': 'https://bundes-klinik-atlas.de/krankenhaussuche/krankenhaus/773491/?tx_tverzhospitaldata_show%5Bquantile%5D=2%2C3%2C6%2C15&tx_tverzhospitaldata_show%5Bsearchlabel%5D=Speiser%C3%B6hren%20und%20Magenkrebs-Operation&tx_tverzhospitaldata_show%5Bsimplesearch%5D=1&tx_tverzhospitaldata_show%5Btreatmentcode%5D=KAOM0&cHash=364a6f260a5792ef6206c30ae1919d11',
            'Prostatakrebs-Operation': 'https://bundes-klinik-atlas.de/krankenhaussuche/krankenhaus/771299/?tx_tverzhospitaldata_show%5Bquantile%5D=15%2C40%2C75%2C127&tx_tverzhospitaldata_show%5Bsearchlabel%5D=Prostatakrebs-Operation&tx_tverzhospitaldata_show%5Bsimplesearch%5D=1&tx_tverzhospitaldata_show%5Btreatmentcode%5D=KAPRK0&cHash=aba8d24f1e9ec2ebcf3ffe761111e997',
            'Pankreaskarzinom-Operation': 'https://bundes-klinik-atlas.de/krankenhaussuche/krankenhaus/771700/?tx_tverzhospitaldata_show%5Bquantile%5D=4%2C7%2C11%2C17&tx_tverzhospitaldata_show%5Bsearchlabel%5D=Pankreaskarzinom-Operation&tx_tverzhospitaldata_show%5Bsimplesearch%5D=1&tx_tverzhospitaldata_show%5Btreatmentcode%5D=KAPK0&cHash=173208dc51def8e0ba8cd9debd9ef268',
            'Totalendoprothese der Hüfte': 'https://bundes-klinik-atlas.de/krankenhaussuche/krankenhaus/772231/?tx_tverzhospitaldata_show%5Bquantile%5D=38%2C77%2C124%2C230&tx_tverzhospitaldata_show%5Bsearchlabel%5D=Totalendoprothese%20der%20H%C3%BCfte&tx_tverzhospitaldata_show%5Bsimplesearch%5D=1&tx_tverzhospitaldata_show%5Btreatmentcode%5D=KAEH0&cHash=efbb9b98461a2830519f76249ec85cb7',
            'Totalendoprothesen-Wechsel der Hüfte': 'https://bundes-klinik-atlas.de/krankenhaussuche/krankenhaus/771358/?tx_tverzhospitaldata_show%5Bquantile%5D=4%2C8%2C14%2C26&tx_tverzhospitaldata_show%5Bsearchlabel%5D=Totalendoprothesen-Wechsel%20der%20H%C3%BCfte&tx_tverzhospitaldata_show%5Bsimplesearch%5D=1&tx_tverzhospitaldata_show%5Btreatmentcode%5D=KARH0&cHash=e4898fb053c6ad37868a99bc9752feb8',
            'Totalendoprothesen-Wechsel des Knies': 'https://bundes-klinik-atlas.de/krankenhaussuche/krankenhaus/771358/?tx_tverzhospitaldata_show%5Bquantile%5D=5%2C10%2C16%2C30&tx_tverzhospitaldata_show%5Bsearchlabel%5D=Totalendoprothesen-Wechsel%20des%20Knies&tx_tverzhospitaldata_show%5Bsimplesearch%5D=1&tx_tverzhospitaldata_show%5Btreatmentcode%5D=KARK0&cHash=7bc10476b7236fa9c4edba6e33c76421',
            'Totalendoprothese des Knies': 'https://bundes-klinik-atlas.de/krankenhaussuche/krankenhaus/771358/?tx_tverzhospitaldata_show%5Bquantile%5D=58%2C93%2C151%2C253&tx_tverzhospitaldata_show%5Bsearchlabel%5D=Totalendoprothese%20des%20Knies&tx_tverzhospitaldata_show%5Bsimplesearch%5D=1&tx_tverzhospitaldata_show%5Btreatmentcode%5D=KAEK0&cHash=03f08c1f87992324d59206f40787b5b5',
            'Behandlung auf einer Schlaganfalleinheit': 'https://bundes-klinik-atlas.de/krankenhaussuche/krankenhaus/771555/?tx_tverzhospitaldata_show%5Bquantile%5D=141%2C350%2C539%2C745&tx_tverzhospitaldata_show%5Bsearchlabel%5D=Behandlung%20auf%20einer%20Schlaganfalleinheit&tx_tverzhospitaldata_show%5Bsimplesearch%5D=1&tx_tverzhospitaldata_show%5Btreatmentcode%5D=KASA0&cHash=ab40287de25dc2cf59c2e637ab1eb940',
            'Multiple Sklerose': 'https://bundes-klinik-atlas.de/krankenhaussuche/krankenhaus/772087/?tx_tverzhospitaldata_show%5Bquantile%5D=1%2C3%2C24%2C57&tx_tverzhospitaldata_show%5Bsearchlabel%5D=Multiple%20Sklerose&tx_tverzhospitaldata_show%5Bsimplesearch%5D=1&tx_tverzhospitaldata_show%5Btreatmentcode%5D=KAMUS0&cHash=cc9e17629f1e9cff7ffb3b678f9c2442',
            'Parkinson': 'https://bundes-klinik-atlas.de/krankenhaussuche/krankenhaus/771912/?tx_tverzhospitaldata_show%5Bquantile%5D=2%2C5%2C12%2C42&tx_tverzhospitaldata_show%5Bsearchlabel%5D=Parkinson&tx_tverzhospitaldata_show%5Bsimplesearch%5D=1&tx_tverzhospitaldata_show%5Btreatmentcode%5D=KAPAR0&cHash=b4c18b572f4841ef85c661036dc1f4c4',
            'Entbindungen': 'https://bundes-klinik-atlas.de/krankenhaussuche/krankenhaus/771984/?tx_tverzhospitaldata_show%5Bquantile%5D=479%2C726%2C1075%2C1695&tx_tverzhospitaldata_show%5Bsearchlabel%5D=Entbindungen&tx_tverzhospitaldata_show%5Bsimplesearch%5D=1&tx_tverzhospitaldata_show%5Btreatmentcode%5D=KAEN0&cHash=147f28b60064cbadb23864ca7d7b01ac',
            'Bauchschlagader: Operation und Stent': 'https://bundes-klinik-atlas.de/krankenhaussuche/krankenhaus/772191/?tx_tverzhospitaldata_show%5Bquantile%5D=4%2C11%2C22%2C34&tx_tverzhospitaldata_show%5Bsearchlabel%5D=Bauchschlagader%3A%20Operation%20und%20Stent%20&tx_tverzhospitaldata_show%5Bsimplesearch%5D=1&tx_tverzhospitaldata_show%5Btreatmentcode%5D=KABAA0&cHash=5dcf8315c289e6dfb45d63e246cc3b56',
            'Durchblutungsstörung der Beine: Operation und Stent': 'https://bundes-klinik-atlas.de/krankenhaussuche/krankenhaus/773318/?tx_tverzhospitaldata_show%5Bquantile%5D=28%2C118%2C204%2C315&tx_tverzhospitaldata_show%5Bsearchlabel%5D=Durchblutungsst%C3%B6rung%20der%20Beine%3A%20Operation%20und%20Stent&tx_tverzhospitaldata_show%5Bsimplesearch%5D=1&tx_tverzhospitaldata_show%5Btreatmentcode%5D=KASCHK0&cHash=9955d47a7543a02d868c6f3cc0b02806',
            'Halsschlagader: Operation und Stent': 'https://bundes-klinik-atlas.de/krankenhaussuche/krankenhaus/772783/?tx_tverzhospitaldata_show%5Bquantile%5D=7%2C19%2C32%2C51&tx_tverzhospitaldata_show%5Bsearchlabel%5D=Halsschlagader%3A%20Operation%20und%20Stent&tx_tverzhospitaldata_show%5Bsimplesearch%5D=1&tx_tverzhospitaldata_show%5Btreatmentcode%5D=KAOH0&cHash=bee2feab4b2c02881380558c5799520c'
            }
    
    return url_dict