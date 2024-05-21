from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
import csv
from io import StringIO
from typing import List, Dict
from collections import defaultdict
import uvicorn

app = FastAPI()

# In-memory data storage
sales_data = []


# Function to calculate statistics
def calculate_statistics():
    total_sales = 0.0
    sales_per_day = defaultdict(float)
    product_sales = defaultdict(int)
    
    for transaction in sales_data:
        total_sales += transaction["amount"]
        sales_per_day[transaction["date"]] += transaction["amount"]
        product_sales[transaction["product_id"]] += transaction["quantity"]
    
    average_sales_per_day = total_sales / len(sales_per_day) if sales_per_day else 0
    
    top_selling_products = sorted(product_sales.items(), key=lambda item: item[1], reverse=True)[:5]
    top_selling_products = [product_id for product_id, quantity in top_selling_products]
    
    return {
        'total_sales': total_sales,
        'average_sales_per_day': average_sales_per_day,
        'top_selling_products': top_selling_products
    }

# Endpoint for file upload
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Read and parse CSV file
    contents = await file.read()
    csv_data = csv.reader(StringIO(contents.decode('utf-8')))
    headers = next(csv_data)
    for row in csv_data:
        transaction = {
            'transaction_id': row[0],
            'date': row[1],
            'product_id': row[2],
            'quantity': int(row[3]),
            'amount': float(row[4])
        }
        sales_data.append(transaction)

    return JSONResponse(status_code=201, content={"message": "File uploaded successfully"})

# Endpoint to get total sales amount
@app.get("/statistics/total_sales_amount")
async def get_total_sales_amount():
    # Calculate total sales amount
    total_sales_amount = sum(transaction['amount'] for transaction in sales_data)
    return {"total_sales_amount": total_sales_amount}

# Endpoint to get average sales per day
@app.get("/statistics/average_sales_per_day")
async def get_average_sales_per_day():
    # Calculate average sales per day
    sales_per_day = defaultdict(float)
    for transaction in sales_data:
        sales_per_day[transaction["date"]] += transaction["amount"]
    average_sales_per_day = sum(sales_per_day.values()) / len(sales_per_day) if sales_per_day else 0
    return {"average_sales_per_day": average_sales_per_day}

# Endpoint to get top selling products
@app.get("/statistics/top_selling_products")
async def get_top_selling_products():

    # Calculate top selling products
    product_sales = defaultdict(int)
    for transaction in sales_data:
        product_sales[transaction["product_id"]] += transaction["quantity"]
    top_selling_products = sorted(product_sales.items(), key=lambda item: item[1], reverse=True)[:5]
    top_selling_products = [{"product_id": product_id, "quantity": quantity} for product_id, quantity in top_selling_products]
    return {"top_selling_products": top_selling_products}


# Main entry point for running the application
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, ssl_keyfile="key.pem", ssl_certfile="cert.pem", ssl_keyfile_password="test")
