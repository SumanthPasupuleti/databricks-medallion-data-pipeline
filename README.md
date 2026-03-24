This project implements an end-to-end data engineering pipeline to integrate data 
from two companies (Raw Fitness and Cbum Fitness) into a unified analytics platform 
using Databricks and Medallion Architecture (Bronze, Silver, Gold).

architecture/project_architecture.png
Source Systems → AWS S3 → Bronze → Silver → Gold → BI / AI

  Data Ingestion
- Data sourced from OLTP systems
- Sportsbar data stored in AWS S3 (Landing Zone)
- Files moved to "processed" folder after ingestion

  Bronze Layer (Raw Data)
- Raw CSV ingestion from S3
- Added metadata:
  - ingestion timestamp
  - source file name

  Silver Layer (Data Cleaning & Transformation)
- Deduplication
- Data standardization (city names, casing)
- Null handling
- Regex-based cleaning
- Column splitting (product, variant)
- Surrogate keys using SHA hashing


 Gold Layer (Business Ready Data)
- Aggregated data for analytics
- Merged Atlon and Sportsbar datasets
- Upsert (merge) logic for incremental updates

Historical Load
- Backfilled 5 months of historical data
- Batch processing
Incremental Load
- Daily ingestion pipeline
- Processes only new data
- Uses staging tables
- Avoids reprocessing historical data


 Data Modeling 
Star Schema Design:
- Fact Table: Orders
- Dimension Tables:
  - Customers
  - Products
  - Dates
  - Pricing

 Orchestration (Make It Clear)
- Orchestrated using Databricks Jobs
- Modular notebooks:
  - customer processing
  - product processing
  - order processing
- Dependency-based execution

   Consumption Layer (Where Business Value Shows)
- Denormalized view created for BI performance
- Used for dashboards and analytics
- Supports:
  - revenue analysis
  - top products
  - sales trends

Project Folder Structure (CRITICAL)
databricks-medallion-pipeline
│
├── notebooks
│   ├── bronze
│   ├── silver
│   └── gold
│
├── ingestion
│   └── s3_ingestion.py
│
├── transformations
│   └── cleaning_logic.py
│
├── sql
│   └── star_schema.sql
│
├── orchestration
│   └── databricks_jobs.json
│
├── architecture
│   └── architecture.png
│
└── README.md

Challenges Faced
- Handling inconsistent city names
- Managing incremental loads without duplication
- Designing surrogate keys

⚡ Improvements / Future Work
- Add streaming pipeline
- Implement CI/CD
- Integrate dbt
