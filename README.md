# Sales Statistics API

This FastAPI application provides endpoints for uploading sales data via CSV files and retrieving various sales statistics.

## Features

- Upload sales data in CSV format.
- Retrieve total sales amount.
- Retrieve average sales per day.
- Retrieve top 5 selling products.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/manvikagaur/File_upload_and_stats.git
   cd File_upload_and_stats
   ```

2. **Create a virtual environment and install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

## Running the Application

Start the FastAPI server:
```bash
python3 app.py 
```

## API Endpoints

- **Upload CSV File:** `POST /upload/`
- **Get Total Sales Amount:** `GET /statistics/total_sales_amount`
- **Get Average Sales Per Day:** `GET /statistics/average_sales_per_day`
- **Get Top Selling Products:** `GET /statistics/top_selling_products`
