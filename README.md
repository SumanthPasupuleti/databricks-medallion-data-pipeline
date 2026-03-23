# databricks-medallion-data-pipeline
This project builds an end-to-end data engineering pipeline to integrate data  from two companies (Raw Fitness and Cbum Fitness) into a unified analytics platform  using Databricks and Medallion Architecture (Bronze, Silver, Gold).

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



# Upgrade Databricks SDK to the latest version and restart Python to see updated packages
%pip install --upgrade databricks-sdk==0.70.0
%restart_python

from databricks.sdk.service.jobs import JobSettings as Job


Product_Incremental_pip = Job.from_dict(
    {
        "name": "Product Incremental pip",
        "schedule": {
            "quartz_cron_expression": "22 0 23 * * ?",
            "timezone_id": "America/Los_Angeles",
            "pause_status": "PAUSED",
        },
        "tasks": [
            {
                "task_key": "dim_processing_customers",
                "notebook_task": {
                    "notebook_path": "/Workspace/Users/sumanthpasupuleti9080@gmail.com/Consolidated_pip/cd Company/Customer data dim processing",
                    "base_parameters": {
                        "catalog": "product",
                        "data_source": "customers",
                    },
                    "source": "WORKSPACE",
                },
            },
            {
                "task_key": "dim_processing_products",
                "depends_on": [
                    {
                        "task_key": "dim_processing_customers",
                    },
                ],
                "notebook_task": {
                    "notebook_path": "/Workspace/Users/sumanthpasupuleti9080@gmail.com/Consolidated_pip/cd Company/products_data_processing",
                    "base_parameters": {
                        "catalog": "product",
                        "data_source": "products",
                    },
                    "source": "WORKSPACE",
                },
            },
            {
                "task_key": "Fact_processing_orders",
                "depends_on": [
                    {
                        "task_key": "dim_processing_pricing",
                    },
                ],
                "notebook_task": {
                    "notebook_path": "/Workspace/Users/sumanthpasupuleti9080@gmail.com/Consolidated_pip/cd Company/3_fact_processing/2_incremental_load_fact",
                    "base_parameters": {
                        "catalog": "product",
                        "data_source": "orders",
                    },
                    "source": "WORKSPACE",
                },
            },
            {
                "task_key": "dim_processing_pricing",
                "depends_on": [
                    {
                        "task_key": "dim_processing_products",
                    },
                ],
                "notebook_task": {
                    "notebook_path": "/Workspace/Users/sumanthpasupuleti9080@gmail.com/Consolidated_pip/cd Company/pricing_data_processing",
                    "base_parameters": {
                        "catalog": "product",
                        "data_source": "gross_price",
                    },
                    "source": "WORKSPACE",
                },
            },
        ],
        "queue": {
            "enabled": True,
        },
        "performance_target": "PERFORMANCE_OPTIMIZED",
    }
)

from databricks.sdk import WorkspaceClient

w = WorkspaceClient()
w.jobs.reset(new_settings=Product_Incremental_pip, job_id=615280701792753)
# or create a new job using: w.jobs.create(**Product_Incremental_pip.as_shallow_dict())


⚡ Improvements / Future Work
- Add streaming pipeline
- Implement CI/CD
- Integrate dbt
