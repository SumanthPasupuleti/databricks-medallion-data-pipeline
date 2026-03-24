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
