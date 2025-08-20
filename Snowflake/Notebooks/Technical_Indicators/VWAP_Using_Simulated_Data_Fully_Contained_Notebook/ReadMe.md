# Technical Analysis with Snowflake Dynamic Tables
- This project demonstrates how to build a powerful, automated data pipeline for calculating stock technical indicators using Snowflake Dynamic Tables. The demo focuses on calculating the Volume Weighted Average Price (VWAP) for AAPL, showcasing an end-to-end workflow from raw data ingestion to interactive visualization.

- The primary goal is to provide a self-contained learning environment for understanding how to replace complex, traditional ETL with a simple, declarative, and reliable data pipeline in Snowflake.

<img width="950" height="279" alt="Screenshot 2025-08-20 at 10 02 06" src="https://github.com/user-attachments/assets/bcf27dbb-2e21-43e0-a751-052acc168d75" />

  
## Pre-requisites
- Please ensure the following packages are included in your Snowflake Notebook:
- dependencies:
  - plotly=6.0.1
  - snowflake=1.6.0
  - snowflake-snowpark-python=1.35.0
  - snowflake.core=1.6.0

<img width="334" height="323" alt="Screenshot 2025-08-20 at 07 35 00" src="https://github.com/user-attachments/assets/73a14711-1b4a-4f66-985c-5257db61f145" />


## Key Features
- ### Declarative Data Pipeline:
  - Replaces complex Streams and Tasks with simple, easy-to-manage Dynamic Tables.

- ### Realistic Data Simulation:
  - Includes a Python Stored Procedure that uses the Geometric Brownian Motion (GBM) financial model to generate a high-fidelity historical dataset, making the demo fully self-contained.

- ### Automated Orchestration:
  - Snowflake automatically manages the entire dependency graph (DAG) and refresh schedule for the pipeline.

- ### Efficient JSON Processing:
  - Demonstrates how to land raw JSON and efficiently flatten it for analysis using LATERAL FLATTEN.

- ### Advanced SQL Analytics:
  - Uses time-series functions (TIME_SLICE) and window functions to perform complex aggregations for VWAP calculation.

- ### Interactive Visualization:
  - Includes a ready-to-run Streamlit dashboard for visual analysis of the results.

## Architecture Overview
The core of this project is a multi-step data pipeline where each transformation layer is a Dynamic Table that automatically refreshes as new data arrives in the upstream source.

<img width="661" height="62" alt="Screenshot 2025-08-16 at 20 39 31" src="https://github.com/user-attachments/assets/04f8bf4a-ff85-4611-b47a-ae15fba2006d" />

- ### Ingestion Table:
  - A standard table (DEMO_MARKET_DATA_JSON_INGESTION_TTBL) where raw, semi-structured JSON data lands.

- ### Normalization DT:
  - The first Dynamic Table (DEMO_TRADE_RECORDS_NORMALIZED_DTBL) reads from the ingestion table, flattens the JSON, and produces clean, structured trade records.

- ### Time Slice DT:
  - The second Dynamic Table (DEMO_VWAP_20MIN_TIME_SLICES_DTBL) aggregates the normalized records into 20-minute windows to calculate an intermediate VWAP.

- ### Cumulative Analysis DT:
  - The final Dynamic Table (DEMO_VWAP_CUMULATIVE_ANALYSIS_DTBL) reads from the time-slice table and uses window functions to calculate the final, cumulative VWAP.

## Technologies Used
### Snowflake:

- #### Dynamic Tables

- #### Snowpark for Python (in a Stored Procedure)

- #### Snowflake SQL

- #### Streamlit-in-Snowflake

## Python Libraries:

- #### NumPy

- #### Plotly

- #### Pandas

## Setup and Usage
This notebook is designed to be run end-to-end within a Snowflake environment.
