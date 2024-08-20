# Hospital Register Project

## Overview

This project aims to analyze and visualize data about hospitals in Germany as provided by the German Governments' *Klinikatlas* website to identify possible differences between the provider types public, private and non-profit.
The project was conducted in the context of the Ironhack Data Analytics Bootcamp I attended from June to August 2024.

**Techniques used in this project**
* Web Scraping & API Requests
* Data Cleaning, Wrangling and Aggregation in Python
* Setting up, Designing and Populating a multi-language Database in MySQL
* Performing Exploratory Data Analysis using SQL queries
* Creating an interactive Streamlit app
<br>

**Demo of the Web App**:

Overview Page           |  Hospital Map with Filter Options
:-------------------------:|:-------------------------:
<img src="resources/app_demo/app_demo_overview.png?raw=true" alt="Demo of the web app" title="Overview Web App Demp" width="400" />  |  <img src="resources/app_demo/app_demo_map.png?raw=true" alt="Demo of the web app" title="Hospital Map Web App Demp" width="550" />

## Data Collection

Data was collected from [bundes-klinik-atlas.de](https://bundes-klinik-atlas.de) using Python with various libraries, such as BeautifulSoup and requests, for both API interactions and web scraping.
In addition, population and area data for the federal states was downloaded from the German authorities [Statistikportal](https://www.statistikportal.de/de/bevoelkerung/flaeche-und-bevoelkerung) website.
In order to map places in Germany to the federal states, data from [opendatasoft](https://public.opendatasoft.com/explore/) was used.
The information about the treatment codes is taken from [VDEK](https://www.vdek.com/vertragspartner/Krankenhaeuser/Datenaustausch/technische_anlagen_2023/_jcr_content/par/download_487520998).

**Klinikatlas API requests**

The list of all hospitals including the following information was retrieved via API requests:
- Name of the hospital
- Address
- Phone number and mail
- Latitude and Longitude
- Link

**Web Scraping Klinikatlas**

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

While conducting the web scraping, the rules of the robots.txt of the website were respected

## Data Processing

- **Cleaning and Organization**: Data was processed and cleaned using Pandas to ensure accuracy and consistency.
- **Database**: The cleaned data was then imported into a MySQL database, created using MySQL Workbench, to facilitate efficient querying and analysis.

<img src="resources/data_processing_sketch/workflow_sketch.svg?raw=true" alt="Sketch of the data processing workflow" title="Workflow Sketch" width="800" />

## Database Design
In order to organize the data, I created a local database using MySQL. The databse is designed in way, such that it can be used for multi-language applications.
The core element of the database is the hospital locations table providing the hospital id as the primary key.

All other tables containing information about individual hospitals, i.e. tables for specific treatments, departments, certificates and other details, refer to this table.
The information in these tables that are linked directly to the hospital locations table is stored by codes, such that it is completely language-agnostic.
In order to make sense of the coding, dictionaries are used. These can be filled with as many translations as desired.
The information containing tables are linked to the dictionaries via code list tables containing the codes as primary keys.

<img src="resources/db/erd.svg?raw=true" alt="Image of the Entity Relationship Diagram (ERD)" title="ERD Model" width="800" />

## Data Analysis and Visualization

**Streamlit App**: An interactive web application was developed using Streamlit to present the data and analysis. The app is still work in progress and not yet deployed.


- **Focus**: The analysis highlights comparisons between different types of hospital providers (public, private, non-profit).
- **Visualizations**: Charts and graphs are used to provide insights and facilitate a better understanding of the data.

<img src="resources/plotly_charts/hospital_size_dist_by_provider_types_2.png" title="Hospital Size Distribution by Provider Types" width="600" />

## Future Work

- Conduct further data analysis (e.g. specialization of hospitals)
- Add more filters to the hospital map (e.g. for certain treatments, certificates and departments)
- Identify places in Germany where the next hospital is more than x driving minutes away and create a map to display the results
- Host the database on a server and deploy the streamlit app
- Create an API to retrieve data from the database and host it on a server
