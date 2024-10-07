
def get_certificate_translation_mapping():
    """
    Summary:
        Get dictionary to translate hospital certificates from German to English

    Arguments:
        None
    
    Returns:
        certificate_translation_mapping (dict): dictionary with German and English translations
    """
    certificate_translation_mapping = {
        "Schlaganfall-Einheit (Stroke Unit)": "Stroke Unit",
        "Darmkrebszentrum": "Colorectal Cancer Center",
        "Zertifiziertes EndoProthetikZentrum": "Certified Endoprosthetics Center",
        "Brustkrebszentrum": "Breast Cancer Center",
        "Gynäkologisches Krebszentrum": "Gynecological Cancer Center",
        "EndoProthetikZentrum der Maximalversorgung": "Endoprosthetics Center of Maximum Care",
        "Onkologisches Zentrum": "Oncology Center",
        "Prostatakrebszentrum": "Prostate Cancer Center",
        "Pankreaskrebszentrum": "Pancreatic Cancer Center",
        "Zentrum für Hämatologische Neoplasien": "Center for Hematologic Neoplasms",
        "Lungenkrebszentrum": "Lung Cancer Center",
        "Zertifiziertes Gefäßzentrum": "Certified Vascular Center",
        "Kopf-Hals-Tumor Krebszentrum": "Head and Neck Tumor Cancer Center",
        "Nierenkrebszentrum": "Kidney Cancer Center",
        "Hautkrebszentrum": "Skin Cancer Center",
        "Zertifiziertes Beckenboden- und Kontinenzzentrum": "Certified Pelvic Floor and Continence Center",
        "Neuroonkologisches Krebszentrum": "Neuro-Oncology Cancer Center",
        "Harnblasenkrebszentrum": "Bladder Cancer Center",
        "Speiseröhrenkrebszentrum": "Esophageal Cancer Center",
        "Magenkrebszentrum": "Stomach Cancer Center",
        "Leberkrebszentrum": "Liver Cancer Center",
        "Zertifizierte Nephrologische Schwerpunktklinik": "Certified Nephrology Specialty Clinic",
        "Sarkomszentrum": "Sarcoma Center",
        "Zertifiziertes Shunt-Referenzzentrum": "Certified Shunt Reference Center",
        "Hodenkrebszentrum": "Testicular Cancer Center",
        "Zertifiziertes Regionales Shuntzentrum": "Certified Regional Shunt Center",
        "EndoProthetikZentrum der Maximalversorgung Schulterendoprothetik": "Endoprosthetics Center of Maximum Care for Shoulder Endoprosthetics",
        "Zertifizierte Nephrologische Schwerpunktklinik/Zentrum für Hypertonie": "Certified Nephrology Specialty Clinic/Center for Hypertension",
        "Zertifiziertes EndoProthetikZentrum Schulterendoprothetik": "Certified Endoprosthetics Center for Shoulder Endoprosthetics",
        "Analkarzinomzentrum": "Anal Carcinoma Center",
        "Zertifizierte Nephrologische Schwerpunktklinik, Zentrum für Hypertonie, Zentrum für Nierentransplantation": "Certified Nephrology Specialty Clinic, Center for Hypertension, Center for Kidney Transplantation",
        "Zertifizierte Schwerpunktklinik, Zentrum für Nierentransplantation": "Certified Specialty Clinic, Center for Kidney Transplantation",
        "EndoProthetikZentrum der Maximalversorgung Schulter-, Tumorendoprothetik und Oberes Sprunggelenk": "Endoprosthetics Center of Maximum Care for Shoulder, Tumor Endoprosthetics and Upper Ankle Joint",
        "Zertifizierte Nephrologische Schwerpunktabteilung": "Certified Nephrology Specialty Department",
        "EndoProthetikZentrum der Maximalversorgung Tumorendoprothetik": "Endoprosthetics Center of Maximum Care for Tumor Endoprosthetics"
    }

    return certificate_translation_mapping


def get_department_translation_mapping():
    """
    Summary:
        Get dictionary to translate hospital departments from German to English

    Arguments:
        None
    
    Returns:
        department_translation_mapping (dict): dictionary with German and English translations
    """
    department_translation_mapping = {
        "Innere Medizin": "Internal Medicine",
        "Herzchirurgie/Intensivmedizin (§ 13 Abs. 2 Satz 3 2. Halbsatz BPflV in der am 31.12.2003 geltenden Fassung)": "Cardiac Surgery/Intensive Care Medicine (§ 13 Abs. 2 Sentence 3 2nd Clause BPflV as of 12/31/2003)",
        "Orthopädie/Schwerpunkt Rheumatologie": "Orthopedics/Specialization in Rheumatology",
        "Orthopädie/Schwerpunkt Chirurgie": "Orthopedics/Specialization in Surgery",
        "Frauenheilkunde/Schwerpunkt Geriatrie": "Gynecology/Specialization in Geriatrics",
        "Frauenheilkunde/Schwerpunkt Hämatologie und internistische Onkologie": "Gynecology/Specialization in Hematology and Internal Oncology",
        "Frauenheilkunde/Schwerpunkt Endokrinologie": "Gynecology/Specialization in Endocrinology",
        "Neurologie/Schwerpunkt Pädiatrie": "Neurology/Specialization in Pediatrics",
        "Neurologie/Schwerpunkt Gerontologie": "Neurology/Specialization in Gerontology",
        "Neurologie/Schwerpunkt Neurologische Frührehabilitation": "Neurology/Specialization in Early Neurological Rehabilitation",
        "Neurologie/Schwerpunkt Schlaganfallpatienten": "Neurology/Specialization in Stroke Patients",
        "Allgemeine Psychiatrie/Schwerpunkt Neurologie": "General Psychiatry/Specialization in Neurology",
        "Allgemeine Psychiatrie/Schwerpunkt Kinder- und Jugendpsychiatrie": "General Psychiatry/Specialization in Child and Adolescent Psychiatry",
        "Allgemeine Psychiatrie/Schwerpunkt Psychosomatik/Psychotherapie": "General Psychiatry/Specialization in Psychosomatics/Psychotherapy",
        "Allgemeine Psychiatrie/Schwerpunkt Suchtbehandlung": "General Psychiatry/Specialization in Addiction Treatment",
        "Allgemeine Psychiatrie/Schwerpunkt Gerontopsychiatrie": "General Psychiatry/Specialization in Geriatric Psychiatry",
        "Allgemeine Psychiatrie/Schwerpunkt Forensische Behandlung": "General Psychiatry/Specialization in Forensic Treatment",
        "Herzchirurgie/Schwerpunkt Thoraxchirurgie/Intensivmedizin": "Cardiac Surgery/Specialization in Thoracic Surgery/Intensive Care Medicine",
        "Herzchirurgie/Schwerpunkt Thoraxchirurgie": "Cardiac Surgery/Specialization in Thoracic Surgery",
        "Pädiatrie/Schwerpunkt Kinderneurologie": "Pediatrics/Specialization in Pediatric Neurology",
        "Herzchirurgie/Schwerpunkt Gefäßchirurgie": "Cardiac Surgery/Specialization in Vascular Surgery",
        "Langzeitbereich Kinder": "Long-Term Care for Children",
        "Kinderkardiologie/Schwerpunkt Intensivmedizin": "Pediatric Cardiology/Specialization in Intensive Care Medicine",
        "Lungen- und Bronchialheilkunde/Schwerpunkt Pädiatrie": "Pulmonology and Bronchial Medicine/Specialization in Pediatrics",
        "Allgemeine Chirurgie/Schwerpunkt Kinderchirurgie": "General Surgery/Specialization in Pediatric Surgery",
        "Allgemeine Chirurgie/Schwerpunkt Unfallchirurgie": "General Surgery/Specialization in Trauma Surgery",
        "Allgemeine Chirurgie/Schwerpunkt Gefäßchirurgie": "General Surgery/Specialization in Vascular Surgery",
        "Allgemeine Chirurgie/Schwerpunkt Plastische Chirurgie": "General Surgery/Specialization in Plastic Surgery",
        "Allgemeine Chirurgie/Schwerpunkt Thoraxchirurgie": "General Surgery/Specialization in Thoracic Surgery",
        "Chirurgie/Schwerpunkt Orthopädie": "Surgery/Specialization in Orthopedics",
        "Allgemeine Chirurgie/Intensivmedizin (§ 13 Abs. 2 Satz 3 2. Halbsatz BPflV in der am 31.12.2003 geltenden Fassung)": "General Surgery/Intensive Care Medicine (§ 13 Abs. 2 Sentence 3 2nd Clause BPflV as of 12/31/2003)",
        "Allgemeine Chirurgie/Schwerpunkt Abdominal- und Gefäßchirurgie": "General Surgery/Specialization in Abdominal and Vascular Surgery",
        "Allgemeine Chirurgie/Schwerpunkt Handchirurgie": "General Surgery/Specialization in Hand Surgery",
        "Thoraxchirurgie/Schwerpunkt Herzchirurgie": "Thoracic Surgery/Specialization in Cardiac Surgery",
        "Thoraxchirurgie/Intensivmedizin": "Thoracic Surgery/Intensive Care Medicine",
        "Thoraxchirurgie/Schwerpunkt Herzchirurgie/Intensivmedizin": "Thoracic Surgery/Specialization in Cardiac Surgery/Intensive Care Medicine",
        "Allgemeine Psychiatrie/Schwerpunkt Suchtbehandlung, Tagesklinik": "General Psychiatry/Specialization in Addiction Treatment, Day Clinic",
        "Allgemeine Psychiatrie/Schwerpunkt Suchtbehandlung, Nachtklinik": "General Psychiatry/Specialization in Addiction Treatment, Night Clinic",
        "Allgemeine Psychiatrie/Schwerpunkt Gerontopsychiatrie, Tagesklinik": "General Psychiatry/Specialization in Geriatric Psychiatry, Day Clinic",
        "Allgemeine Psychiatrie/Schwerpunkt Gerontopsychiatrie, Nachtklinik": "General Psychiatry/Specialization in Geriatric Psychiatry, Night Clinic",
        "Intensivmedizin/Schwerpunkt Frauenheilkunde und Geburtshilfe": "Intensive Care Medicine/Specialization in Gynecology and Obstetrics",
        "Intensivmedizin/Schwerpunkt Hals-, Nasen-, Ohrenheilkunde": "Intensive Care Medicine/Specialization in Otorhinolaryngology",
        "Intensivmedizin/Schwerpunkt Neurologie": "Intensive Care Medicine/Specialization in Neurology",
        "Operative Intensivmedizin/Schwerpunkt Chirurgie": "Operative Intensive Care Medicine/Specialization in Surgery",
        "Intensivmedizin/Thorax-Herzchirurgie": "Intensive Care Medicine/Thoracic-Cardiac Surgery",
        "Intensivmedizin/Herz-Thoraxchirurgie": "Intensive Care Medicine/Cardiac-Thoracic Surgery",
        "Angiologie": "Angiology",
        "Radiologie": "Radiology",
        "Palliativmedizin": "Palliative Medicine",
        "Schmerztherapie": "Pain Therapy",
        "Heiltherapeutische Abteilung": "Therapeutic Department",
        "Wirbelsäulenchirurgie": "Spine Surgery",
        "Suchtmedizin": "Addiction Medicine",
        "Visceralchirurgie": "Visceral Surgery",
        "Weaningeinheit": "Weaning Unit",
        "Intensivmedizin/Schwerpunkt Urologie": "Intensive Care Medicine/Specialization in Urology",
        "Intensivmedizin/Schwerpunkt Herzchirurgie": "Intensive Care Medicine/Specialization in Cardiac Surgery",
        "Intensivmedizin/Schwerpunkt Chirurgie": "Intensive Care Medicine/Specialization in Surgery",
        "Psychosomatik/Psychotherapie/Nachtklinik (für teilstationäre Pflegesätze)": "Psychosomatics/Psychotherapy/Night Clinic (for partial inpatient care rates)",
        "Allgemeine Psychiatrie/Tagesklinik (für teilstationäre Pflegesätze)": "General Psychiatry/Day Clinic (for partial inpatient care rates)",
        "Allgemeine Psychiatrie/Nachtklinik (für teilstationäre Pflegesätze)": "General Psychiatry/Night Clinic (for partial inpatient care rates)",
        "Kinder- und Jugendpsychiatrie/Tagesklinik (für teilstationäre Pflegesätze)": "Child and Adolescent Psychiatry/Day Clinic (for partial inpatient care rates)",
        "Kinder- und Jugendpsychiatrie/Nachtklinik (für teilstationäre Pflegesätze)": "Child and Adolescent Psychiatry/Night Clinic (for partial inpatient care rates)",
        "Psychosomatik/Psychotherapie/Schwerpunkt Kinder- und Jugendpsychosomatik": "Psychosomatics/Psychotherapy/Specialization in Child and Adolescent Psychosomatics",
        "Psychosomatik/Psychotherapie/Tagesklinik (für teilstationäre Pflegesätze)": "Psychosomatics/Psychotherapy/Day Clinic (for partial inpatient care rates)",
        "Nuklearmedizin/Schwerpunkt Strahlenheilkunde": "Nuclear Medicine/Specialization in Radiation Therapy",
        "Intensivmedizin/Schwerpunkt Neurochirurgie": "Intensive Care Medicine/Specialization in Neurosurgery",
        "Strahlenheilkunde/Schwerpunkt Hämatologie und internistische Onkologie": "Radiation Therapy/Specialization in Hematology and Internal Oncology",
        "Strahlenheilkunde/Schwerpunkt Radiologie": "Radiation Therapy/Specialization in Radiology",
        "Dermatologie/Tagesklinik (für teilstationäre Pflegesätze)": "Dermatology/Day Clinic (for partial inpatient care rates)",
        "Intensivmedizin/Schwerpunkt Innere Medizin": "Intensive Care Medicine/Specialization in Internal Medicine",
        "Intensivmedizin/Schwerpunkt Kardiologie": "Intensive Care Medicine/Specialization in Cardiology",
        "Intensivmedizin/Schwerpunkt Pädiatrie": "Intensive Care Medicine/Specialization in Pediatrics",
        "Pädiatrie/Schwerpunkt Perinatalmedizin": "Pediatrics/Specialization in Perinatal Medicine",
        "Pädiatrie/Schwerpunkt Lungen- und Bronchialheilkunde": "Pediatrics/Specialization in Pulmonology and Bronchial Medicine",
        "Geriatrie": "Geriatrics",
        "Thoraxchirurgie": "Thoracic Surgery",
        "Urologie": "Urology",
        "Orthopädie": "Orthopedics",
        "Frauenheilkunde und Geburtshilfe": "Gynecology and Obstetrics",
        "Geburtshilfe": "Obstetrics",
        "Hals-, Nasen-, Ohrenheilkunde": "Otorhinolaryngology",
        "Augenheilkunde": "Ophthalmology",
        "Neurologie": "Neurology",
        "Allgemeine Psychiatrie": "General Psychiatry",
        "Kinder- und Jugendpsychiatrie": "Child and Adolescent Psychiatry",
        "Psychosomatik/Psychotherapie": "Psychosomatics/Psychotherapy",
        "Nuklearmedizin": "Nuclear Medicine",
        "Strahlenheilkunde": "Radiation Therapy",
        "Dermatologie": "Dermatology",
        "Zahn- und Kieferheilkunde, Mund- und Kieferchirurgie": "Dentistry and Oral and Maxillofacial Surgery",
        "Intensivmedizin": "Intensive Care Medicine",
        "Herzchirurgie": "Cardiac Surgery",
        "Plastische Chirurgie": "Plastic Surgery",
        "Pädiatrie/Schwerpunkt Neonatologie": "Pediatrics/Specialization in Neonatology",
        "Gefäßchirurgie": "Vascular Surgery",
        "Kardiologie": "Cardiology",
        "Nephrologie": "Nephrology",
        "Hämatologie und internistische Onkologie": "Hematology and Internal Oncology",
        "Endokrinologie": "Endocrinology",
        "Gastroenterologie": "Gastroenterology",
        "Pneumologie": "Pulmonology",
        "Rheumatologie": "Rheumatology",
        "Pädiatrie": "Pediatrics",
        "Kinderkardiologie": "Pediatric Cardiology",
        "Neonatologie": "Neonatology",
        "Kinderchirurgie": "Pediatric Surgery",
        "Lungen- und Bronchialheilkunde": "Pulmonology and Bronchial Medicine",
        "Allgemeine Chirurgie": "General Surgery",
        "Unfallchirurgie": "Trauma Surgery",
        "Neurochirurgie": "Neurosurgery",
        "Orthopädie und Unfallchirurgie": "Orthopedics and Trauma Surgery",
        "Frauenheilkunde": "Gynecology",
        "Sonstige Fachabteilung": "Other Specialty Department",
        "Innere Medizin/Schwerpunkt Geriatrie": "Internal Medicine/Specialization in Geriatrics",
        "Nephrologie/Intensivmedizin": "Nephrology/Intensive Care Medicine",
        "Hämatologie und internistische Onkologie/Schwerpunkt Pädiatrie": "Hematology and Internal Oncology/Specialization in Pediatrics",
        "Hämatologie und internistische Onkologie/Schwerpunkt Frauenheilkunde": "Hematology and Internal Oncology/Specialization in Gynecology",
        "Hämatologie und internistische Onkologie/Schwerpunkt Strahlenheilkunde": "Hematology and Internal Oncology/Specialization in Radiation Therapy",
        "Endokrinologie/Schwerpunkt Gastroenterologie": "Endocrinology/Specialization in Gastroenterology",
        "Endokrinologie/Schwerpunkt Pädiatrie": "Endocrinology/Specialization in Pediatrics",
        "Gastroenterologie/Schwerpunkt Endokrinologie": "Gastroenterology/Specialization in Endocrinology",
        "Gastroenterologie/Schwerpunkt Pädiatrie": "Gastroenterology/Specialization in Pediatrics",
        "Rheumatologie/Schwerpunkt Pädiatrie": "Rheumatology/Specialization in Pediatrics",
        "Pädiatrie/Schwerpunkt Nephrologie": "Pediatrics/Specialization in Nephrology",
        "Pädiatrie/Schwerpunkt Hämatologie und internistische Onkologie": "Pediatrics/Specialization in Hematology and Internal Oncology",
        "Pädiatrie/Schwerpunkt Endokrinologie": "Pediatrics/Specialization in Endocrinology",
        "Pädiatrie/Schwerpunkt Gastroenterologie": "Pediatrics/Specialization in Gastroenterology",
        "Pädiatrie/Schwerpunkt Rheumatologie": "Pediatrics/Specialization in Rheumatology",
        "Pädiatrie/Schwerpunkt Kinderkardiologie": "Pediatrics/Specialization in Pediatric Cardiology",
        "Nephrologie/Schwerpunkt Pädiatrie": "Nephrology/Specialization in Pediatrics",
        "Geriatrie/Nachtklinik (für teilstationäre Pflegesätze)": "Geriatrics/Night Clinic (for partial inpatient care rates)",
        "Geriatrie/Tagesklinik (für teilstationäre Pflegesätze)": "Geriatrics/Day Clinic (for partial inpatient care rates)",
        "Innere Medizin/Schwerpunkt Rheumatologie": "Internal Medicine/Specialization in Rheumatology",
        "Innere Medizin/Schwerpunkt Kardiologie": "Internal Medicine/Specialization in Cardiology",
        "Innere Medizin/Schwerpunkt Nephrologie": "Internal Medicine/Specialization in Nephrology",
        "Innere Medizin/Schwerpunkt Hämatologie und internistische Onkologie": "Internal Medicine/Specialization in Hematology and Internal Oncology",
        "Innere Medizin/Schwerpunkt Endokrinologie": "Internal Medicine/Specialization in Endocrinology",
        "Innere Medizin/Schwerpunkt Gastroenterologie": "Internal Medicine/Specialization in Gastroenterology",
        "Innere Medizin/Schwerpunkt Pneumologie": "Internal Medicine/Specialization in Pulmonology",
        "Innere Medizin/Schwerpunkt Lungen- und Bronchialheilkunde": "Internal Medicine/Specialization in Pulmonology and Bronchial Medicine",
        "Geriatrie/Schwerpunkt Frauenheilkunde": "Geriatrics/Specialization in Gynecology",
        "Innere Medizin/Tumorforschung": "Internal Medicine/Tumor Research",
        "Innere Medizin/Schwerpunkt Coloproktologie": "Internal Medicine/Specialization in Coloproctology",
        "Innere Medizin/Schwerpunkt Infektionskrankheiten": "Internal Medicine/Specialization in Infectious Diseases",
        "Innere Medizin/Schwerpunkt Diabetes": "Internal Medicine/Specialization in Diabetes",
        "Innere Medizin/Schwerpunkt Naturheilkunde": "Internal Medicine/Specialization in Naturopathy",
        "Innere Medizin/Schwerpunkt Schlaganfallpatienten": "Internal Medicine/Specialization in Stroke Patients",
        "Schmerztherapie/Tagesklinik": "Pain Therapy/Day Clinic"
    }

    return department_translation_mapping


def get_treatment_translation_list():
    """
    Summary:
        Get list of treatments in English

    Arguments:
        None
    
    Returns:
        treatment_translation_list (list): list with English translations
    """
    treatment_translation_list = [
    "Surgical Heart Valve Replacement",
    "Minimally Invasive Heart Valve Replacement",
    "Heart Bypass Surgery",
    "Cardiac Catheterization with Stent",
    "Pneumonia",
    "Breast Cancer Surgery",
    "Lung Cancer Surgery",
    "Colon Cancer Surgery",
    "Esophageal and Stomach Cancer Surgery",
    "Prostate Cancer Surgery",
    "Pancreatic Cancer Surgery",
    "Total Hip Replacement",
    "Hip Revision Surgery",
    "Knee Revision Surgery",
    "Total Knee Replacement",
    "Treatment in a Stroke Unit",
    "Multiple Sclerosis",
    "Parkinson's Disease",
    "Childbirth",
    "Abdominal Aortic Aneurysm: Surgery and Stent",
    "Peripheral Artery Disease: Surgery and Stent",
    "Carotid Artery: Surgery and Stent"
    ]

    return treatment_translation_list


def get_federal_states_translation_list():
    """
    Summary:
        Get list of German federal states in English

    Arguments:
        None

    Returns:
        federal_states_translation_list (list): list with English translations
    """

    federal_states_translation_list = [
    "Baden-Württemberg",
    "Bavaria",
    "Berlin",
    "Brandenburg",
    "Bremen",
    "Hamburg",
    "Hesse",
    "Lower Saxony",
    "Mecklenburg-Western Pomerania",
    "North Rhine-Westphalia",
    "Rhineland-Palatinate",
    "Saarland",
    "Saxony",
    "Saxony-Anhalt",
    "Schleswig-Holstein",
    "Thuringia"
    ]

    return federal_states_translation_list