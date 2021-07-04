import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
data=pd.read_csv('../data/processed_data_alatauski.csv')
data['year_of_building']=data['year_of_building'].astype(float,errors='raise')
# incorrect=data[data['year_of_building']==3.].index
# data=data.drop(index=incorrect)
print(data['year_of_building'].unique())
data.to_csv('../data/processed_data_alatauski.csv',index=False)