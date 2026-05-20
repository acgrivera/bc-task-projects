import numpy as np
import pandas as pd

sales_month = {
        'Monday':[200,250,120,500],
        'Tuesday':[100,200,None,400],
        'Wednesday':[100,200,300,400],
        'Thursday':[100,None,300,400],
        'Friday':[900,899,121,None]
}

sales = pd.DataFrame(sales_month)
check_sales = sales.isna().sum()
clean_sales = sales.fillna(0) #function ok change None to zero, if set to zero
#clean_sales = sales.fillna(sales.mean()) #returns mean to missing values
#drop_sales = sales.dropna()
#sales #returnError

print(check_sales)