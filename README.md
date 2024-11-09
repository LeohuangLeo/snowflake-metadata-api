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
```

## API Endpoints

Here’s a breakdown of the available API endpoints.

### 1. **Get All Schemas in a Database**
- **Endpoint**: `GET /schemas/{database}`
- **Parameters**:  
    - `database`: The name of the Snowflake database.
- **Response**:  
    A list of schema names in the specified database.

**Example Request**:

```bash
curl http://127.0.0.1:8000/schemas/my_database
```

### 2. Get Table Metadata
- **Endpoint**: `GET /table-metadata/{database}/{schema}/{table}`
- **Parameters**:
  - `database`: The name of the Snowflake database.
  - `schema`: The name of the schema within the database.
  - `table`: The name of the table whose metadata you wish to retrieve.

- **Description**:  
  This endpoint returns metadata for the specified table in a given schema and database. The metadata includes column names, data types, and descriptions (if available).

- **Response**:  
  A list of dictionaries, where each dictionary contains the column name, data type, and description of the column.

**Example Request**:

```bash
curl http://127.0.0.1:8000/table-metadata/my_database/my_schema/my_table
```

### Get Table Metrics
- **Endpoint**: `GET /table-metrics/{database}/{schema}/{table}`
- **Parameters**:
  - `database`: The name of the Snowflake database.
  - `schema`: The name of the schema within the database.
  - `table`: The name of the table whose metrics you want to retrieve.

- **Description**:  
  This endpoint returns summary statistics for each column in the specified table. It provides different types of statistics based on the column data types:

  - For **numeric columns** (e.g., `NUMBER`, `INTEGER`, `DECIMAL`, `FLOAT`, `DOUBLE`), the following statistics will be calculated:
    - Non-null count
    - Mean (average)
    - Minimum value
    - Maximum value

  - For **non-numeric columns** (e.g., `VARCHAR`, `TEXT`, `DATE`), the following statistics will be provided:
    - Non-null count
    - Unique count

  These statistics help you understand the distribution and completeness of the data in your table.

- **Response**:  
  A dictionary where each key is a column name and its value is another dictionary containing various statistics for that column.

**Example Request**:

```bash
curl http://127.0.0.1:8000/table-metrics/my_database/my_schema/my_table
```

<img width="857" alt="image" src="https://github.com/user-attachments/assets/c21f2008-5a15-4863-ae12-ef685205e949">
<img width="854" alt="image" src="https://github.com/user-attachments/assets/eb270bcd-40a2-4627-9d2c-0dc32f870aa7">
<img width="850" alt="image" src="https://github.com/user-attachments/assets/7d88eecb-037a-4308-89d1-b53ed01601fb">



## Q&A

- **It tooks me approximately 3.5 hours to complete the project.**
- **It's a interesting project to work with as snowflake is a well-known datawarehouse and I get a chance to work and play around with it.**
- **Next Step**
 - Add test cases.
 - Optimize the way to query the snowflake table to get metrics.
 - Add more details annotation in codebase. e.g., add comment on class and function explain the funtionality of it.
 - Onboard github action flow to making sure the build and quality of repo.
 - Load testing: Checking the perfomance of each individual api call to make sure it can support enough loading.

