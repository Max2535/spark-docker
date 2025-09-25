param(
    [int]$TimeoutSeconds = 180
)

$containerName = "spark-master"
$initScriptPath = "/docker-entrypoint-initdb.d/init.sql"

Write-Host "=== Waiting for $containerName to be ready ==="
$deadline = (Get-Date).AddSeconds($TimeoutSeconds)
$running = $false

while ((Get-Date) -lt $deadline) {
    $inspectOutput = docker inspect -f '{{.State.Status}}' $containerName 2>$null
    if ($LASTEXITCODE -eq 0 -and $inspectOutput -eq 'running') {
        $running = $true
        break
    }
    Start-Sleep -Seconds 5
}

if (-not $running) {
    throw "Container '$containerName' is not running. Start the stack with 'docker compose up -d' first."
}

Write-Host "=== Verifying init script is present at $initScriptPath ==="
& docker exec $containerName test -f $initScriptPath
if ($LASTEXITCODE -ne 0) {
    throw "Init script not found at $initScriptPath inside $containerName."
}

Write-Host "=== Executing init script against Spark master ==="
$execArgs = @(
    "exec",
    $containerName,
    "/opt/bitnami/spark/bin/spark-sql",
    "--master", "spark://spark-master:7077",
    "-i", $initScriptPath
)
& docker @execArgs
if ($LASTEXITCODE -ne 0) {
    throw "spark-sql exited with a non-zero code."
}

Write-Host "=== Finished running init.sql ==="
