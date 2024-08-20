# Hospital Data Analytics Project

## Overview

This project aims to analyze and visualize data about hospitals in Germany to understand the differences between various provider types (public, private, non-profit). The data was gathered using a combination of API calls and web scraping from [bundes-klinik-atlas.de](https://bundes-klinik-atlas.de).

## Data Collection

- **Sources**: Data was collected from [bundes-klinik-atlas.de](https://bundes-klinik-atlas.de) using Python for both API interactions and web scraping.
- **Tools**: Python libraries for web scraping (e.g., BeautifulSoup, requests) and API interaction.

## Data Processing

- **Cleaning and Organization**: Data was processed and cleaned using Pandas to ensure accuracy and consistency.
- **Database**: The cleaned data was then imported into a MySQL database, created using MySQL Workbench, to facilitate efficient querying and analysis.

## Database Design

<img src="db/erd_model.svg?raw=true" alt="Image of the Entity Relationship Diagram (ERD)" title="ERD Model" width="800" />


## Data Analysis and Visualization

- **Streamlit App**: An interactive web application was developed using Streamlit to present the data and analysis.
- **Focus**: The analysis highlights comparisons between different types of hospital providers (public, private, non-profit).
- **Visualizations**: Charts and graphs are used to provide insights and facilitate a better understanding of the data.

## Future Work

The database contains extensive data that can be explored further for more in-depth analysis and insights.
