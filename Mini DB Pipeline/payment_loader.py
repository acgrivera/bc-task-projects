import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine(
"postgresql+psycopg2://postgres:password@localhost:5432/quickcash_dw"
)
def load_new_payments(engine):
    print("Reading new payments file...")
    new_payments_df = pd.read_csv("data/new_payments.csv")
    print("Loading data to staging")
    new_payments_df.to_sql(
        "payments_staging",
        engine,
        if_exists="replace",
        index=False
    )
    print("Staging Load Complete!")
    insert_to_fact_query = """
INSERT INTO fact_payments (payment_id,fact_loan_id, payment_amount,payment_date)
SELECT payment_id, loan_id, payment_amount, cast(payment_date as date)
FROM payments_staging
on conflict (payment_id) do nothing
"""
    with engine.begin() as conn:
        conn.execute(text(insert_to_fact_query))
    print("Payments inserted to fact table")
    print("Generating loan payment report")

    report_query = """
    SELECT
        f.fact_loan_id,
        c.customer_name, 
        f.loan_amount,
        COALESCE(SUM(p.payment_amount),0) AS total_payments,
        f.loan_status
        FROM fact_loans f
    LEFT JOIN fact_payments p ON f.fact_loan_id = p.fact_loan_id
    JOIN dim_customers c ON f.customer_id = c.customer_id
    GROUP BY f.fact_loan_id,c.customer_name,f.loan_amount,f.loan_status
    """

    report_df = pd.read_sql(report_query,engine)
    report_df.to_csv("reports/loan_payment_report.csv",index=False)

        
# print(df_loans)
def loan_details(engine):
    query = """
    SELECT
        f.fact_loan_id,
        c.customer_name,
        p.product_name,
        f.loan_amount,
        f.loan_status
    from fact_loans f
    join dim_customers c on f.customer_id = c.customer_id
    join dim_loan_products p on f.product_id = p.product_id
    """

    df = pd.read_sql(query,engine)
    return df

def get_total_payments(engine):
    payments = pd.read_sql("SELECT * FROM fact_payments",engine)
    return payments["payment_amount"].sum()

def loan_progress_report(engine):
    query = """
    SELECT
        f.fact_loan_id,
        f.loan_amount,
        SUM(p.payment_amount) AS total_payments
        from fact_loans f
        left join fact_payments p on f.fact_loan_id = p.fact_loan_id
        group by f.fact_loan_id, f.loan_amount
"""
    df = pd.read_sql(query,engine)
    df["payment_percentage"] = (df["total_payments"] / df["loan_amount"]) * 100
    filtered_df = df[df["fact_loan_id"].isin([149,150,164])] 
    return filtered_df   
# print(loan_details(engine=engine))
print(loan_progress_report(engine=engine))

# load_new_payments(engine=engine)
# print(get_total_payments(engine=engine))