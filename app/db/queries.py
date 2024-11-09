def show_schemas_query(database):
    """SQL query to show schemas in the current database."""
    return f"SHOW SCHEMAS IN DATABASE {database}"


def show_tables_query(schema_name: str, database: str):
    """SQL query to show tables in a given schema."""
    return f"SHOW TABLES IN SCHEMA {database}.{schema_name}"

def show_table_info(table_name: str, schema_name: str, databse: str):
    """SQL query to show table info in a given table."""
    return f"""
        describe table {databse}.{schema_name}.{table_name}
        """