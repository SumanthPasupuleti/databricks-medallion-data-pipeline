# Databricks notebook source
# DBTITLE 1,Setup: Use Catalog Product
# MAGIC %sql
# MAGIC USE CATALOG product;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE SCHEMA if not exists product.gold; 
# MAGIC CREATE SCHEMA if not exists product.silver;
# MAGIC CREATE SCHEMA if not exists product.bronze;

# COMMAND ----------

