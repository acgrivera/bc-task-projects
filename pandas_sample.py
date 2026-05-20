import pandas as pd

sales_index = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
sales_values = [500, 200, 300, 200, 100]

#sales_series = pd.Series(sales_values)
sales_series = pd.Series(sales_values, index=sales_index)

print(sales_series)
