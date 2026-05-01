# Complementar Clientes

## Overview

This project complements and cleans client information using Python. The main goal is to prepare a more complete client dataset by combining available client data with production or business information.

## Business Problem

Client data can come from different sources and may not always have the same structure. Some files may be missing columns, contain inconsistent formatting, or require additional information before they can be used for analysis or reporting.

This project helps create a cleaner and more complete client dataset.

## Tools Used

- Python
- pandas
- pathlib
- Excel files
- CSV files
- Parquet files

## What I Did

- Loaded client and production data
- Compared available columns with expected columns
- Identified missing columns before combining data
- Cleaned text fields and identification fields
- Standardized important columns
- Combined client information into a final structured dataset
- Added validation prints to understand the process during execution

## Main Features

- Column validation before concatenation
- Detection of missing columns
- Cleaning of client names and identification fields
- Standardized output structure
- Debug messages to verify if the process worked correctly

## Why This Project Matters

This project makes the client data more reliable and easier to use in later analysis. It also helps avoid errors when different promoters or files have different column structures.

## Conclusion

This project helped improve data quality by validating, cleaning, and complementing client information before using it in dashboards or other business processes.
