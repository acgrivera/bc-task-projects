import psycopg2
import pandas as pd
from datetime import datetime

#DB connection (PostgreSQL)
DB_Config = {
        "dbname": "pc_store",
        "user": "postgres",
        "password": "1234",
        "host": "localhost",
        "port": "5435",
}

def create_db_design():
    """
    Retail DB Design
    - proucts and sales tables
    """
    conn = psycopg2.connect(**DB_Config)
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS products (
                product_id SERIAL PRIMARY KEY,
                product_name VARCHAR(255) NOT NULL,
                price DECIMAL(10, 2) NOT NULL
    );
    CREATE TABLE IF NOT EXISTS sales (
                sale_id SERIAL PRIMARY KEY,
                product_id INTEGER REFERENCES products(product_id),
                quantity INTEGER NOT NULL,
                sale_date DATE NOT NULL
    );
''')
    cur.execute('''
    INSERT INTO products (product_name, price)
    VALUES
                ('RGB GAMING MOUSE', 799.99),
                ('MECHANICAL KEYBOARD', 8500.00),
                ('27-IN GAMING MONITOR', 12000.00)            
''')

    conn.commit()
    cur.close()
    conn.close()
    print("Database Design Created.")

def run_data_pipeline(product_id, quantity):
    """
    Data Pipeline
    DB for transactions
    """
    conn = psycopg2.connect(**DB_Config)
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO sales (product_id, quantity, sale_date)
    VALUES (%s, %s, %s);
    ''', (product_id, quantity, datetime.now()))
    conn.commit()
    cur.close()
    print("Pipeline Executed.")

def sales_reporting_engine():
    conn = psycopg2.connect(**DB_Config)

    query = '''
    SELECT
        p.product_name,
        SUM(s.quantity) AS total_items_sold,
        SUM(s.quantity * p.price) AS "Total_Revenue"
    FROM
        sales s
    JOIN products p ON s.product_id = p.product_id
    GROUP BY
        p.product_name
    ORDER BY
        "Total Revenue" DESC;
'''

    df = pd.read_sql(query, conn)
    conn.close()
    df.to_csv ('reports/daily_sales_report.csv', index=False)
    print("Report has been generated successfully.")


#create_db_design()

#run_data_pipeline(2,2)
#run_data_pipeline(1,24)
#run_data_pipeline(3,10)
#sales_reporting_engine