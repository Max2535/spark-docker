import requests

# API endpoints
BACKEND_URL = "http://localhost:8000"
UPLOAD_URL = f"{BACKEND_URL}/upload"
QUERY_URL = f"{BACKEND_URL}/query"

# ตัวอย่างไฟล์ CSV สำหรับทดสอบ
TEST_FILE = "sales.csv"
with open(TEST_FILE, "w") as f:
    f.write("id,product,amount\n")
    f.write("1,Apple,1200\n")
    f.write("2,Banana,500\n")
    f.write("3,Orange,800\n")
    f.write("4,Apple,2200\n")
    f.write("5,Mango,1500\n")

# Step 1: Upload CSV
with open(TEST_FILE, "rb") as f:
    files = {"file": (TEST_FILE, f, "text/csv")}
    res = requests.post(UPLOAD_URL, files=files)
    print("UPLOAD RESPONSE:", res.status_code, res.json())

# Step 2: Run Spark SQL Query
query = """
SELECT product, SUM(amount) AS total_sales
FROM sales
GROUP BY product
ORDER BY total_sales DESC
"""
res = requests.post(QUERY_URL, data={"query": query})
print("QUERY RESPONSE:", res.status_code)
print("RESULT JSON:", res.json())
