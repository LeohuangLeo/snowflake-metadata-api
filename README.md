# Snowflake Data API

This FastAPI application allows you to interact with Snowflake and retrieve metadata, schema information, and statistical metrics about tables in your Snowflake databases. The API includes endpoints to list schemas, get metadata for tables, and retrieve summary statistics for each column in a table.

## Features

- **Get Schemas**: Fetch a list of all schemas in a specific Snowflake database.
- **Get Table Metadata**: Fetch column names, data types, and descriptions for a given table in a specified schema and database.
- **Get Table Metrics**: Retrieve summary statistics for each column in a table, including counts, averages, min, max, and unique counts for numeric and non-numeric columns.
- **Health Check**: A simple endpoint to check if the API server is up and running.

## Prerequisites

Before running this application, ensure you have the following installed:

- **Python 3.8+**
- **pip** (Python's package installer)

You'll also need the **Snowflake** Python connector, which is required to interact with Snowflake databases.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/snowflake-api.git
    cd snowflake-api
    ```

2. Set up a virtual environment (optional but recommended):

    ```bash
    python3 -m venv venv
    source venv/bin/activate   # On Windows, use venv\Scripts\activate
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Ensure that you have a Snowflake account and valid credentials (user, password, role, database, warehouse).

## Configuration

You may need to adjust your Snowflake credentials and other configurations. These can be defined in your code or through environment variables.

- **Snowflake Connection**: In `app/db/connection.py`, ensure the Snowflake credentials are correct (account, user, password, etc.).

For example:
```python
# app/db/connection.py
import snowflake.connector

def get_snowflake_connection(database: str):
    conn = snowflake.connector.connect(
        user='your_username',
        password='your_password',
        account='your_account',
        role='your_role',
        warehouse='your_warehouse',
        database=database,
        schema='your_schema',
    )
    return conn
