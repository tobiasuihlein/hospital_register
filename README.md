# Hospital Register Project
This project aims to analyze and visualize data about hospitals in Germany as provided by the German governments' *Klinikatlas* website. It is a continuation of my final project for the Ironhack Data Analytics Bootcamp.

### Techniques used in this project
* Web Scraping & API Requests
* Data Cleaning, Wrangling and Aggregation in Python
* Setting up, Designing and Populating a multi-language Database in MySQL
* Performing Exploratory Data Analysis using SQL queries
* Creating an interactive Web App using Django
* Deploying the Web App on local Server using Docker

### Demo of the Web App
A MVP Version of the Web App can be found [here](https://hospital.hermiantor.eu/) (ask me for credentials).

Data Visuals Page           |  Hospital Search Map with Filter Options
:-------------------------:|:-------------------------:
<img src="resources/images/app_demo/django_app_data_2.png?raw=true" alt="Demo image of the django web app" title="Data Charts Web App Demo" width="400" /> | <img src="resources/images/app_demo/django_app_search.png?raw=true" alt="Demo image of the django web app" title="Search Web App Demo" width="520" />

## Data Collection
Data was collected from [bundes-klinik-atlas.de](https://bundes-klinik-atlas.de) using Python with various libraries, such as BeautifulSoup and requests, for both API interactions and web scraping.
In addition, population and area data for the federal states was downloaded from the German authorities [Statistikportal](https://www.statistikportal.de/de/bevoelkerung/flaeche-und-bevoelkerung) website.
In order to map places in Germany to the federal states, data from [opendatasoft](https://public.opendatasoft.com/explore/) was used.
The information about the treatment codes is taken from [VDEK](https://www.vdek.com/vertragspartner/Krankenhaeuser/Datenaustausch/technische_anlagen_2023/_jcr_content/par/download_487520998).

### Klinikatlas API requests
The list of all hospitals including the following information was retrieved via API requests:
- Name of the hospital
- Address
- Phone number and mail
- Latitude and Longitude

 ### Web Scraping Klinikatlas
Klinikatlas provides various data about hospitals in Germany, of which the following were gathered via web scraping:
- Provider type
- Number of beds
- Number of semi-residential stations
- Total number of treatments
- Nursing quotient and nursing count
- Emergency service level
- Number of specific selected treatments
- Number of treatments in a specific department
- Certificates

## Data Processing
The data retrieved via API requests and web scraping is cleaned, aggregated and manipulated using Pandas.
As an example, hospital departments were encoded to ensure consistency and provide the possibilty for multi-language applications.
In the final step of data wrangling, the data was brought to CSV files corresponding to the tables to be used in the database.

<img src="data_processing/resources/data_processing_sketch/workflow_sketch.svg?raw=true" alt="Sketch of the data processing workflow" title="Workflow Sketch" width="800" />

## Database Design
To organize the data, I created a local MySQL database. The database is designed to support **multi-language** applications. The core element is the hospital locations table, which serves the hospital id as the primary key.

All other tables containing information about individual hospitals, such as treatments, departments, certificates, and other details, reference via hospital id to this primary table.
The linked information in these tables is stored using codes to ensure language-independence. To interpret the codes, dictionary tables are utilized, which can accommodate any number of translations.
The information-containing tables are then linked to the dictionaries via code list tables, where the codes act as the primary keys.

<img src="data_processing/resources/db/erd.svg?raw=true" alt="Image of the Entity Relationship Diagram (ERD)" title="ERD Model" width="800" />

## Data Analysis and Visualization
For the analysis, SQL queries were used to retrieve specific data from the database.
With a Python script, this data is then brought into Pandas dataframes and visualized using the Plotly library.
The created charts are then displayed in a Django web application, which is yet to be deployed together with the database.

For now, in the analysis, I focused on comparisons between the different types of hospital providers.
The figures below show some examples of the charts.

### Hospital Size Distribution and Nursing Quotient
The charts show that private hospitals tend to be smaller in size compared to public and non-profit ones.
Regarding the number of patients per nursing staff, private hospitals show a distribution of wider spread, i.e. there are hospitals with a significantly smaller, but also ones with a larger ratio.

<img src="data_processing/resources/plotly_charts/hospital_size_dist_by_provider_types_2.png" title="Hospital Size Distribution by Provider Types" width="400" />   <img src="data_processing/resources/plotly_charts/nursing_quotient_by_provider_type.png" title="Nursing Quotient Distribution by Provider Types" width="400" />

### Number of Hospitals per Capita
Among the federal states, the number of hospitals per capita shows a wide spread.
While the state with the lowest has only 3.6 hospitals per 1000 inhabitantes, the state with the highest number has almost twice as much.

Also the states differ significantly in their shares of different provider types.
While some states have only very minor number of or even no private hospitals at all, for others private hospitals make up to half of the total number.

<img src="data_processing/resources/plotly_charts/hospital_beds_per_1000_capita_by_provider_type.png" title="Hospital Beds per 1000 Capita by Provider Types" width="600" />

## Future Work

- Conduct further data analysis (e.g. specialization of hospitals)
- Add more filters to the hospital map (e.g. for certain treatments or certificates)
- Create feature finding the nearest hospital for given coordinates

## Links

[Presentation Slides](https://slides.com/d/jMVsFKI/live) <br>
[Bundes-Klinik-Atlas](https://bundes-klinik-atlas.de) <br>
[Web App MVP](https://hospital.hermiantor.eu)
