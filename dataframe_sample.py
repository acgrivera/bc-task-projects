import numpy as np
import pandas as pd

sales_month = {
        'Monday':[200,250,120,500],
        'Tuesday':[100,200,300,400],
        'Wednesday':[100,200,300,400],
        'Thursday':[100,200,300,400],
        'Friday':[900,899,121,949]
}
week_index = ['week1', 'week2', 'week3', 'week4']
test_series = pd.DataFrame(sales_month, week_index)
#test_series["weekly_total"] = test_series.sum(axis=1)  #for weekly total
#test_series.loc["day_total"] = test_series.sum(axis=0) #for daily total

#print(test_series) #'test_series.T' to transpose

#iloc - index locate
#print(test_series.iloc[2:3,3:4])

test_series['Saturday']=[100,200,300,400]   #add Saturday and values
new_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
test_series= test_series.reindex(columns=new_order)
test_series["weekly_total"] = test_series.sum(axis=1)
print(test_series)
#test_series.drop("weekly_total")   #removes weekly total