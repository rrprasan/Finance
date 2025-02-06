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

Step 1: Click on the "+" Icon in Snowsight -> Select "Table" -> Select "From File"

<img width="380" alt="Screenshot 2025-02-06 at 04 55 13" src="https://github.com/user-attachments/assets/bb667461-224c-4a2c-b945-2e05974f7657" />

Step 2: You will see the "Load Data Into File" Pop-up Window.

<img width="752" alt="Screenshot 2025-02-06 at 04 55 29" src="https://github.com/user-attachments/assets/0b1556a4-ce8c-4535-966f-49f647842b75" />

Step 3: Drop the "SBS_Certified_Business_List_20250206.csv" file into the "Load Data Into File" Window. Select your database and schema and name your table as NYC_SMALL_BUSINESS_TBL 
<img width="751" alt="Screenshot 2025-02-06 at 04 56 13" src="https://github.com/user-attachments/assets/f7ceea19-daab-483d-a5ba-07f6ab1f8769" />

Step 4: Press "Next" on the "Load Data Into File" Pop-up Window. 
<img width="1303" alt="Screenshot 2025-02-06 at 04 56 44" src="https://github.com/user-attachments/assets/eb821586-a5e9-47ec-882e-1c1f493afa30" />
Step 5: You will find that there are 4 errors in the Column Names. The Column Names created by NYC have Spaces in them. You scroll down to the columns with the errors or have Snowflake auto-fix the error. I fixed the errors by replacing the spaces with underscores and removing any "(" characters in the column name.     
<img width="1299" alt="Screenshot 2025-02-06 at 04 57 27" src="https://github.com/user-attachments/assets/7ea2c2da-17ab-405f-89a7-084120d8ae2e" />
** IMPORTANT NOTE **
Step 6: Please ensure you change the LATITUDE and LONGITUDE Data Types from NUMBER to FLOAT.   
<img width="1300" alt="Screenshot 2025-02-06 at 04 58 25" src="https://github.com/user-attachments/assets/ef1df86d-7cb9-4d7d-a079-935183c7a87c" />







