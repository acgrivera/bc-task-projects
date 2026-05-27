"""
CSV -> cleaning, transformation (Pyspark) psycopg2
dependencies: Pyspak and Psycopg2
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, monotonically_increasing_id, expr, sum as _sum, count, round
import psycopg2

conn = psycopg2.connect(
    host = "localhost",
    database = "dpwh_db",
    user = "postgres",
    password = "1234",
    port = "5435"
)

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS flood_control_summary (
        id SERIAL PRIMARY KEY,
        region VARCHAR(255),
        total_projects INT,
        total_budget NUMERIC(20, 2),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""")
conn.commit()
cursor.close()
conn.close()


spark = SparkSession.builder \
    .appName("DPWH_FloodControl_etl") \
    .config("spark.jars.packages", "org.postgresql:postgresql:42.5.4") \
    .getOrCreate()

df = spark.read.csv("dpwh_flood_control_projects.csv", header=True, inferSchema=True)
#df.show(5)

#df.printSchema()

df_cast = df.withColumn("ContractCost", col("ContractCost").try_cast("double"))

df_clean = df_cast.filter(col("Region").isNotNull()) \
    .filter(col("ContractCost").isNotNull()) \
    .filter(col("ContractCost")>0)

df_removed = df_cast.filter(
    col("Region").isNull() | 
    col("ContractCost").isNull() | 
    (col("ContractCost") <= 0)
)

df_raw = df.count()
df_clean_count = df_clean.count()
df_removed_count = df_removed.count()

#print(f"""
#        raw df record count: {df_raw},
#        clean record count: {df_clean_count},
#        removed record count: {df_removed_count}""")

df_indexed = df_removed.withColumn("row_idx", monotonically_increasing_id())

print("\n--- Sample of Removed Records ---")
#df_indexed.select("row_idx", "ProjectID", "Region", "ContractCost").show(50, truncate=False)
df_non_numeric = df_indexed.filter(col("ContractCost").isNotNull() & expr("try_cast(ContractCost as double)").isNull())

df_proof = df.filter(col("ProjectID") == "P00521541VS")

df_proof.select("ProjectID", "ProjectName", "TypeOfWork", "FundingYear", "ContractId", "ApprovedBudgetForContract", "ContractCost").show(truncate=False)

df_transformed = df_clean.withColumn("cost_millions", round(col("ContractCost")/1000000, 2))

summary_df = df_transformed.groupBy("Region").agg(
    count("*").alias("total_projects"),
    _sum('ContractCost').alias("total_budget"))

summary_df.show(truncate=False)

#pandas_df = summary_df.toPandas()

print("\n--- Loading Summary Metrics to PostgreSQL ---")
conn = psycopg2.connect(
    host = "localhost",
    database = "dpwh_db",
    user = "postgres",
    password = "1234",
    port = "5435"
)
cursor = conn.cursor()

#for row in pandas_df.itertuples():
#    cursor.execute("""
#        INSERT INTO flood_control_summary (region, total_projects, total_budget)
#        VALUES (%s, %s, %s)       
#    """, (row.Region, row.total_projects, row.total_budget))

#conn.commit()   
#cursor.close()
#conn.close()

summary_df.write.format("jdbc").option("url", "jdbc:postgresql://localhost:5435/dpwh_db") \
    .option("dbtable", "flood_control_summary") \
    .option("user", "postgres") \
    .option("password", "1234") \
    .option("driver", "org.postgresql.Driver") \
    .mode("overwrite") \
    .save()