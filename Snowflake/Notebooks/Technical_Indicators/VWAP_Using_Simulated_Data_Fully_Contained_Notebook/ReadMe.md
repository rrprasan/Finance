# Technical Analysis with Snowflake Dynamic Tables
- This project demonstrates how to build a powerful, automated data pipeline for calculating stock technical indicators using Snowflake Dynamic Tables. The demo focuses on calculating the Volume Weighted Average Price (VWAP) for AAPL, showcasing an end-to-end workflow from raw data ingestion to interactive visualization.

- The primary goal is to provide a self-contained learning environment for understanding how to replace complex, traditional ETL with a simple, declarative, and reliable data pipeline in Snowflake.

## Key Features
- ### Declarative Data Pipeline: Replaces complex Streams and Tasks with simple, easy-to-manage Dynamic Tables.

- ### Realistic Data Simulation: Includes a Python Stored Procedure that uses the Geometric Brownian Motion (GBM) financial model to generate a high-fidelity historical dataset, making the demo fully self-contained.

- ### Automated Orchestration: Snowflake automatically manages the entire dependency graph (DAG) and refresh schedule for the pipeline.

- ### Efficient JSON Processing: Demonstrates how to land raw JSON and efficiently flatten it for analysis using LATERAL FLATTEN.

- ### Advanced SQL Analytics: Uses time-series functions (TIME_SLICE) and window functions to perform complex aggregations for VWAP calculation.

- ### Interactive Visualization: Includes a ready-to-run Streamlit dashboard for visual analysis of the results.

## Architecture Overview
The core of this project is a multi-step data pipeline where each transformation layer is a Dynamic Table that automatically refreshes as new data arrives in the upstream source.

- ### Ingestion Table: A standard table (DEMO_MARKET_DATA_JSON...) where raw, semi-structured JSON data lands.

- ### Normalization DT: The first Dynamic Table (DEMO_TRADE_RECORDS_NORMALIZED_DTBL) reads from the ingestion table, flattens the JSON, and produces clean, structured trade records.

- ### Time Slice DT: The second Dynamic Table (DEMO_VWAP_20MIN_TIME_SLICES_DTBL) aggregates the normalized records into 20-minute windows to calculate an intermediate VWAP.

- ### Cumulative Analysis DT: The final Dynamic Table (DEMO_VWAP_CUMULATIVE_ANALYSIS_DTBL) reads from the time-slice table and uses window functions to calculate the final, cumulative VWAP.

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
