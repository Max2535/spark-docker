import io
import os
from typing import List

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pyspark.sql import SparkSession
import pandas as pd

app = FastAPI()

SPARK_MASTER_URL = os.getenv("SPARK_MASTER_URL", "spark://spark-master:7077")
RESULT_ROW_LIMIT = int(os.getenv("RESULT_ROW_LIMIT", "100"))

spark = (
    SparkSession.builder
    .appName("CSVUploader")
    .master(SPARK_MASTER_URL)
    .getOrCreate()
)

# Permissive CORS for demo; tighten in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Read uploaded CSV into memory
        content = await file.read()
        if not content:
            return JSONResponse(status_code=400, content={"detail": "Empty file"})

        # Parse with pandas to infer schema (numeric types, etc.)
        text_stream = io.StringIO(content.decode("utf-8", errors="ignore"))
        pdf = pd.read_csv(text_stream)

        # Create Spark DataFrame and register as temp view
        table_name = os.path.splitext(os.path.basename(file.filename))[0]
        # Sanitize table name: letters, numbers, underscore only
        table_name = "".join(c if c.isalnum() or c == "_" else "_" for c in table_name)
        if not table_name:
            table_name = "uploaded_table"

        df = spark.createDataFrame(pdf)
        df.createOrReplaceTempView(table_name)

        # Preview first few rows
        preview_limit = min(5, RESULT_ROW_LIMIT)
        preview_rows = [row.asDict(recursive=True) for row in df.limit(preview_limit).collect()]

        return {
            "message": f"Registered '{table_name}' as a temporary view with {df.count()} rows",
            "tableName": table_name,
            "columns": df.columns,
            "preview": preview_rows,
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"Upload failed: {e}"})


@app.post("/query")
async def run_query(query: str = Form(...)):
    try:
        df = spark.sql(query)
        limited = df.limit(RESULT_ROW_LIMIT)
        data = [row.asDict(recursive=True) for row in limited.collect()]
        return {
            "columns": df.columns,
            "data": data,
            "limit": RESULT_ROW_LIMIT,
        }
    except Exception as e:
        return JSONResponse(status_code=400, content={"detail": f"Query error: {e}"})
