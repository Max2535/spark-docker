# PowerShell script to run init.sql in Spark Master

Write-Host "=== Starting Spark init.sql execution ==="

# รอ master ขึ้น (ตรวจสอบด้วย docker ps)
Start-Sleep -Seconds 10

# รัน spark-sql พร้อมส่ง init.sql
docker exec -it spark /opt/bitnami/spark/bin/spark-sql `
  --master spark://spark:7077 `
  -i /docker-entrypoint-initdb.d/init.sql

Write-Host "=== Finished running init.sql ==="
