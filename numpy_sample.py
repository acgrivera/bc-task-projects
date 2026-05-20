import numpy as np
import pandas as pd

#s = pd.Series(np.random.randn(10))
#print(s)

sales = {'Monday':500, 'Tuesday':200, 'Wednesday':300, 'Thursday':150, 'Friday':175}

sales_series_dict = pd.Series(sales)

#Specific values
#print(sales_series_dict[0]) #Error not accepted
#print(sales_series_dict['Monday']) #accepted

#[[]] Gets index and value
#print(sales_series_dict[[0]]) #Error not accepted
#print(sales_series_dict[['Monday']]) #accepted
#print(sales_series_dict[sales_series_dict == 150]) #accepted

# [:] Returns start up to specified index
#print(sales_series_dict[:3]) #accepted

#[n,n,n]
#print(sales_series_dict[[0, 2, 4]]) #Error not accepted
#print(sales_series_dict.iloc[[0, 2, 4]]) #accepted

#[condition]
#print(sales_series_dict[sales_series_dict>=300]) #accepted

print(sales_series_dict + sales_series_dict) #accepted