## Comparing Annual Share Repurchases Across Companies Using Snowflake PIVOT function.
### Author: [Prasanna Rajagopal](https://www.linkedin.com/in/prasannarajagopal/)

## [PIVOT](https://docs.snowflake.com/en/sql-reference/constructs/pivot)

Rotates a table by turning the unique values from one column in the input expression into multiple columns and aggregating results where required on any remaining column values. In a query, it is specified in the FROM clause after the table name or subquery.

The operator supports the built-in aggregate functions AVG, COUNT, MAX, MIN, and SUM.

PIVOT can be used to transform a narrow table (for example, empid, month, sales) into a wider table (for example, empid, jan_sales, feb_sales, mar_sales).


## The PIVOT function is particularly valuable when:

1. Comparing multiple entities
2. Analyzing time-series data
3. Creating executive dashboards
4. Preparing data for visualization
5. Conducting competitive analysis
