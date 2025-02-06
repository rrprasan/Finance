# Visualizing New York City Small Business on a Map Using Snowflake Notebook
## You will learn the following from this Snowflake Notebook:
## Snowflake provides the following data types for geospatial data:

### The [GEOGRAPHY](https://docs.snowflake.com/en/sql-reference/data-types-geospatial#geography-data-type) data type, which models Earth as though it were a perfect sphere.
#### Points on the earth are represented as degrees of longitude (from -180 degrees to +180 degrees) and latitude (-90 to +90). Snowflake uses 14 decimal places to store GEOGRAPHY coordinates.

### The [GEOMETRY](https://docs.snowflake.com/en/sql-reference/data-types-geospatial#geometry-data-type) data type, which represents features in a planar (Euclidean, Cartesian) coordinate system.
#### The coordinates are represented as pairs of real numbers (x, y). Currently, only 2D coordinates are supported.
# Analyze New York City Small Business Data Using Snowflake Geospatial Functions.
## Goals
### 1. Convert LATITUDE & LONGITUDE in FLOAT to GEOGRAPHY Data Type. 
### 2. Aggregate all the small business locations for a selected sales territory.
### 3. Create a minimum bounding box (Envelope) that encompasses the small businesses in a territory. 
### 4. Display the Box and the small businesses located within that box. 
## Steps:
### 1. Create GEOGRAPHY Data Type for Each New York City Small Business Using [ST_MAKEPOINT](https://docs.snowflake.com/en/sql-reference/functions/st_makepoint)
### 2. Aggregate the GEOGRAPHY Points for the Sales Territory of your Choice Using [ST_COLLECT](https://docs.snowflake.com/en/sql-reference/functions/st_collect) For eg.: Bronx
### 3. Convert to GEOMETRY Data Type for Easy Envelope (Box) Creation Using [TO_GEOMETRY](https://docs.snowflake.com/en/sql-reference/functions/to_geometry)
### 4. Create Envelope (minimum bounding box) With the GEOMETRY Object Using [ST_ENVELOPE](https://docs.snowflake.com/en/sql-reference/functions/st_envelope)
### 5. Find the Center of the Envelope for Proper Positioning on the Map Using [ST_CENTROID](https://docs.snowflake.com/en/sql-reference/functions/st_centroid)
### 6. Layer the Envelope & Bronx Small Business GEOGRAPHY Points on the Map Using PyDeck.  

Follow the following steps to import the NYC Small Business CSV Data into Snowflake.  

<img width="380" alt="Screenshot 2025-02-06 at 04 55 13" src="https://github.com/user-attachments/assets/bb667461-224c-4a2c-b945-2e05974f7657" />



