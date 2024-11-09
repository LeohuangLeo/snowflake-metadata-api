from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from typing import List, Dict
from .services.snowflake_service import SnowflakeService
from app.db.connection import get_snowflake_connection

app = FastAPI()


# Instantiate SnowflakeService to handle the DB interactions
snowflake_service = SnowflakeService()

@app.get("/schemas/{database}", response_model=List[str])
async def get_schemas(database: str):
    try:
        return snowflake_service.get_schemas(database)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/table-metadata/{database}/{schema}/{table}", response_model=List[dict])
async def get_table_metadata(database: str, schema: str, table: str):
    """
    Fetch all columns (name, data type, description) for a specific table in a schema of a database.
    """
    try:
        return snowflake_service.get_table_metadata(table, schema, database)
    
    except Exception as e:
        print(f"Error fetching tables: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get("/table-metrics/{database}/{schema}/{table}") #Dict[str, Dict[str, float]]
async def get_table_metrics(database: str, schema: str, table: str):
    try:
        return snowflake_service.get_table_metrics(table, schema, database)
    
    except Exception as e:
        print(f"Error fetching tables: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")




@app.get("/health")
async def health_check():
    return {"status": "OK"}
