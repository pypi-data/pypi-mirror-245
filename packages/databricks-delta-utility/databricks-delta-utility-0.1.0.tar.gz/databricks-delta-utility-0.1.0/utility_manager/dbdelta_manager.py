# my_databricks_package/my_databricks/dbdelta_manager.py

import os
import json
import logging
import pyspark.sql as spark
from delta.tables import DeltaTable

class DatabricksDeltaTableManager:
    def __init__(self, spark_session, mount_path=None, catalog=None):
        self.spark = spark_session
        self.mount_path = mount_path or "/mnt/delta_tables"
        self.catalog = catalog or "spark_catalog"
        self.config_path = os.path.join(self.mount_path, "config.json")
        self.logger = self.setup_logger()
        self.load_config()

    def setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger

    def load_config(self):
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, "r") as config_file:
                    self.config = json.load(config_file)
            else:
                self.config = {"tables": {}}
        except Exception as e:
            self.logger.error(f"Error loading config: {str(e)}")
            raise

    def save_config(self):
        try:
            with open(self.config_path, "w") as config_file:
                json.dump(self.config, config_file, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving config: {str(e)}")
            raise

    def get_workspace_info(self):
        try:
            # Implement logic to get Databricks workspace information
            # For example, use Databricks REST API or other suitable methods
            workspace_info = {"workspace_id": "your_workspace_id", "user": "current_user"}
            return workspace_info
        except Exception as e:
            self.logger.error(f"Error getting workspace information: {str(e)}")
            raise

    def create_delta_table(self, table_name, suffix=None, prefix=None):
        try:
            full_table_name = f"{prefix}_{table_name}_{suffix}".strip("_")
            if full_table_name in self.config["tables"]:
                raise ValueError(f"Table '{full_table_name}' already exists.")

            workspace_info = self.get_workspace_info()

            # Implement logic to create Delta table using SQL commands
            delta_table_path = os.path.join(self.mount_path, full_table_name)
            self.spark.sql(f"CREATE TABLE {self.catalog}.{full_table_name} USING DELTA LOCATION '{delta_table_path}'")

            # Update config with the new table information
            self.config["tables"][full_table_name] = {
                "table_name": full_table_name,
                "workspace_id": workspace_info["workspace_id"],
                "user": workspace_info["user"],
                "catalog": self.catalog,
            }
            self.save_config()

            self.logger.info(f"Delta table '{full_table_name}' created successfully.")
            return f"Delta table '{full_table_name}' created successfully."
        except Exception as e:
            self.logger.error(f"Error creating Delta table: {str(e)}")
            raise

    def delete_delta_table(self, table_name):
        try:
            if table_name not in self.config["tables"]:
                raise ValueError(f"Table '{table_name}' does not exist.")

            # Implement logic to delete Delta table using SQL commands
            full_table_name = table_name
            self.spark.sql(f"DROP TABLE IF EXISTS {self.catalog}.{full_table_name}")

            # Remove table information from config
            del self.config["tables"][table_name]
            self.save_config()

            self.logger.info(f"Delta table '{table_name}' deleted successfully.")
            return f"Delta table '{table_name}' deleted successfully."
        except Exception as e:
            self.logger.error(f"Error deleting Delta table: {str(e)}")
            raise

    def list_delta_tables(self):
        try:
            return list(self.config["tables"].keys())
        except Exception as e:
            self.logger.error(f"Error listing Delta tables: {str(e)}")
            raise
