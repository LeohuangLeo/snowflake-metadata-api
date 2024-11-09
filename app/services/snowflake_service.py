from app.db.connection import get_snowflake_connection
from app.db.queries import show_schemas_query, show_tables_query, show_table_info
from app.utils.helper import clean_data_type
from fastapi import HTTPException

class SnowflakeService:

    def _execute_query(self, query: str, database: str):
        """ Helper function to execute a query and return the results. """
        conn = None
        cursor = None
        try:
            conn = get_snowflake_connection(database)
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Exception as e:
            raise Exception(f"Error executing query: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_schemas(self, database: str):
        """ Get all schemas for a given database. """
        try:
            schemas_query = show_schemas_query(database)
            result = self._execute_query(schemas_query, database)
            if not result:
                raise HTTPException(status_code=404, detail="No schemas found")
            # Filter out None values and return schema names
            schemas = [row[1] for row in result if row[1] is not None]
            return schemas
        except Exception as e:
            raise Exception(f"Error fetching schemas: {str(e)}")

    def get_table_metadata(self, table_name: str, schema_name: str, database: str):
        """ Get metadata (column names, data types, description) for a given table. """
        try:
            table_info_query = show_table_info(table_name, schema_name, database)
            columns = self._execute_query(table_info_query, database)
            if not columns:
                raise HTTPException(status_code=404, detail=f"No columns found for {table_name} in schema {schema_name} of database {database}")
            
            # Format the result into a list of dictionaries
            column_info = [
                {"column_name": row[0], "data_type": row[1], "description": row[9] or "No description"}
                for row in columns
            ]
            return column_info
        except Exception as e:
            raise Exception(f"Error fetching metadata for table {table_name}: {str(e)}")

    def get_table_metrics(self, table_name: str, schema_name: str, database: str):
        """ Get summary statistics (e.g., non-null count, mean, min, max, unique count) for each column. """
        try:
            # Get column metadata first
            table_info_query = show_table_info(table_name, schema_name, database)
            columns = self._execute_query(table_info_query, database)

            column_stats = {}
            for column in columns:
                column_name, data_type = column[0], clean_data_type(column[1])

                # Determine the type of metrics to fetch based on the column data type
                if data_type in ('NUMBER', 'INTEGER', 'DECIMAL', 'FLOAT', 'DOUBLE'):
                    column_stats[column_name] = {
                        "non_null_count": f"COUNT({column_name})",
                        "mean": f"AVG({column_name})",
                        "min": f"MIN({column_name})",
                        "max": f"MAX({column_name})"
                    }
                else:
                    column_stats[column_name] = {
                        "non_null_count": f"COUNT({column_name})",
                        "unique_count": f"COUNT(DISTINCT {column_name})"
                    }

            # Execute queries to get statistics for each column
            result_dict = {}
            for column_name, metrics in column_stats.items():
                query = self._build_column_stats_query(schema_name, table_name, column_name, metrics)
                result = self._execute_query(query, database)
                
                # The results will be a single row of statistics per column
                result_dict[column_name] = {
                    "non_null_count": result[0][1],
                    "mean": result[0][2],
                    "min": result[0][3],
                    "max": result[0][4],
                    "unique_count": result[0][5]
                }

            return result_dict

        except Exception as e:
            raise Exception(f"Error fetching metrics for table {table_name}: {str(e)}")

    def _build_column_stats_query(self, schema_name: str, table_name: str, column_name: str, metrics: dict):
        """ Helper function to build the SQL query for a single column's statistics. """
        col_name = f"'{column_name}' AS column_name"
        col_non_null_count = f"{metrics['non_null_count']} AS non_null_count" if "non_null_count" in metrics else "null AS non_null_count"
        col_unique_count = f"{metrics['unique_count']} AS unique_count" if "unique_count" in metrics else "null AS unique_count"
        col_mean = f"{metrics['mean']} AS mean_" if "mean" in metrics else "null AS mean_"
        col_min = f"{metrics['min']} AS min_" if "min" in metrics else "null AS min_"
        col_max = f"{metrics['max']} AS max_" if "max" in metrics else "null AS max_"

        # Construct the query
        return f"""
        SELECT {col_name}, {col_non_null_count}, {col_unique_count}, {col_mean}, {col_min}, {col_max}
        FROM {schema_name}.{table_name}
        """

