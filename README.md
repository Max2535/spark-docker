# Spark Docker

End-to-end environment for experimenting with Apache Spark through a FastAPI backend and React frontend, all orchestrated with Docker Compose.

## Prerequisites

- Docker Desktop (or Docker Engine + Docker Compose plugin)
- PowerShell 7+ (for the helper script on Windows)

## Stack Overview

- **Spark master** (`bitnami/spark:3.5.0`) with a worker container
- **FastAPI backend** container exposing `http://localhost:8000`
- **React frontend** container exposing `http://localhost:3000`
- Bind-mounted `./data` directory shared with Spark and the backend for CSV imports
- Optional SQL bootstrap script in `./init/init.sql`

## Quick Start

```powershell
# Build images (only required the first time or after changes)
docker compose build

# Start the full stack in the background
docker compose up -d

# Optional: load the sample CSVs into Spark SQL catalog
powershell -ExecutionPolicy Bypass -File .\run-init.ps1
```

Open the following URLs after the containers are running:

- Frontend app: <http://localhost:3000>
- Backend OpenAPI docs: <http://localhost:8000/docs>
- Spark master web UI: <http://localhost:8080>

To watch logs:

```powershell
# Tail backend logs
docker compose logs -f backend

# Tail Spark master logs
docker compose logs -f spark-master
```

Shut everything down with:

```powershell
docker compose down -v
```

## Uploading Data and Running Queries

1. Use the web UI to upload a CSV file (or `curl` against `/upload`). Files are loaded into a Spark DataFrame and registered as a temporary view for the current backend session (no HDFS required). The name of the view is based on the file name (e.g., `sales.csv` -> table `sales`).
2. Run SQL queries via the UI or by invoking the `/query` endpoint with form data (`query=SELECT ...`). Results are capped at 100 rows by default.

The upload endpoint returns a preview of the data so you can quickly inspect the first few rows before querying.

## Configuration

Environment variables you can override in `docker-compose.yml` or container settings:

- `SPARK_MASTER_URL` - spark master URL used by the backend (defaults to `spark://spark-master:7077`)
- `RESULT_ROW_LIMIT` - maximum number of rows returned from `/query` (default `100`)
- `SPARK_CONNECT_ATTEMPTS` / `SPARK_CONNECT_BACKOFF_SECONDS` - tune backend retries while waiting for Spark
- `REACT_APP_API_BASE_URL` - frontend base URL for API calls (defaults to `http://localhost:8000`)

 Modify `init/init.sql` to pre-create databases or tables. The script is executed against the running Spark master using `run-init.ps1`.

### Notes

- Uploaded CSVs are held in-memory and as temp views in the Spark session of the backend. If the backend restarts, re-upload files before querying.
- The `./data` folder is mounted into Spark containers for convenience if you prefer to read from files directly (e.g., `spark.read.csv('file:///data/your.csv')`). The backend's upload flow does not depend on it.

### Rebuild after changes

```powershell
docker compose build backend; docker compose up -d backend
```

If you encounter errors like `SparkFileNotFoundException: File file:/app/uploads/... does not exist`, ensure you're not pointing Spark at a container-local path that isn't shared with executors. Use temp views from the upload flow or a shared path like `file:///data/...` that is mounted to all Spark containers.

## Troubleshooting

- Ensure the Spark master container is healthy before running the init script; the script waits up to 3 minutes by default.
- If you see `Unable to connect to Spark master` from the backend, confirm port `7077` is reachable and restart the backend container after Spark is up.
- For file permission issues, verify the Docker Desktop file sharing settings include the project directory.

## Project Structure

```
spark-docker/
  backend/
    Dockerfile
    requirements.txt
    server.py
  data/
    products.csv
    sales.csv
  frontend/
    Dockerfile
    package.json
    src/
  init/
    init.sql
  docker-compose.yml
  run-init.ps1
  README.md
```
