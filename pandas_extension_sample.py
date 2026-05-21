import pandas as pd

#DataFrame:
#Column - Category
#Row - Record

data = {
    "product":["Laptop", "Mouse", "Keyboard", "Monitor"],
    "price":[1200.50, 25.00, 45.99, 3500.00],
    "quantity":[2, 20, 10, 5]
}
#For hardcoded data
df = pd.DataFrame(data)

df["total_sales"] = df["price"] * df["quantity"]    #New column "total_sales"
ts = df.groupby("product", as_index=False)["total_sales"].sum()
ts = ts.sort_values(by="total_sales", ascending=False)
ts.to_csv('sales_by_product.csv')
print(df.sort_values("total_sales", ascending=False))
#print(df)

#Data from file
#df = pd.read_csv("Sample Data/raw_sales_data.csv")
#print(df)    #df.head() returns sample of the dataframe

#print(df[(df["Amount"]>1000) & (df["customer_id"] == "C001")])     #returns the specific data for the assigned logical expression


