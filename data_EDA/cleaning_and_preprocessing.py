from typing import no_type_check
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt

full_data = pd.read_csv('../data/raw_data_nauryzbaiski.csv',header=None,names=['number_of_rooms','Price','Floor','area','description'])
print(full_data.shape)

def find_number(text):
    num = re.findall(r'\d+(?:\.\d+)?',text)
    return " ".join(num)
full_data['Price']=full_data['Price'].apply(lambda x:find_number(x))
full_data['Price']=full_data['Price'].str.replace(' ','').astype(float)

full_data['Floor']=(full_data['Floor'].apply(lambda x: str(x).split('этаж')[0].strip())).str.replace(' ',"")
full_data['Total_Floor']=full_data['Floor'].apply(lambda x: str(x).split('/',1)[-1])
full_data['Floor']=full_data['Floor'].apply(lambda x: str(x).split('/')[0])

full_data['area']=full_data['area'].apply(lambda x:find_number(x))
full_data['area']=full_data['area'].str.replace(' ','').astype(float)

full_data['residential_complex']= full_data['description'].str.extract(r'жил. комплекс (.*?),')

full_data['house_type']= full_data['description'].str.extract(r', (кирпичный|панельный|монолитный) ')

full_data['year_of_building']= full_data['description'].str.extract(r', (\d.*?) г.п., ')

full_data['Ceiling']= full_data['description'].str.extract(r', потолки (.*?)м., ')

full_data['bathroom_unit']=full_data['description'].str.extract(r' санузел (.*?), ')

full_data['furniture']=full_data['description'].str.extract(r', (пустая|частично меблирована|полностью меблирована), ')

print(full_data[['number_of_rooms','area','Floor','Total_Floor','Ceiling','furniture','bathroom_unit','house_type','year_of_building','Price']].duplicated().mean())
''' 7 percent of duplicates'''
full_data=full_data.drop_duplicates(subset=['number_of_rooms','area','Floor','Total_Floor','Ceiling','furniture','bathroom_unit','house_type','year_of_building','Price'])

''' handling incorrect Prices'''
incorrect_prices=full_data[full_data['Price']<1000000].index
full_data = full_data.drop(index=incorrect_prices)
incorrect_prices=full_data[full_data['Price']>1000000000].index
full_data = full_data.drop(index=incorrect_prices)


''' handling incorrect area'''

incorrect_area=full_data[full_data['area']<10].index
full_data = full_data.drop(index=incorrect_area)
incorrect_area=full_data[full_data['area']>500].index
full_data = full_data.drop(index=incorrect_area)

'''handling incorrect number or room '''
print(full_data['number_of_rooms'].value_counts())


'''handling incorrect residential complex'''
print(full_data['residential_complex'].value_counts())

'''handling incorrect ceiling'''
full_data['Ceiling']=full_data['Ceiling'].astype(float)
incorrect_ceiling=full_data[full_data['Ceiling']<1].index
full_data = full_data.drop(index=incorrect_ceiling)
incorrect_ceiling=full_data[full_data['Ceiling']>10].index
full_data = full_data.drop(index=incorrect_ceiling)

'''handling incorrect bathroom unit'''
print(full_data['bathroom_unit'].value_counts())


'''handling incorrect year of building'''
# full_data['year_of_building']=full_data['year_of_building'].astype(float)
# incorrect_year=full_data[full_data['year_of_building']<1950].index
# full_data = full_data.drop(index=incorrect_year)
# incorrect_year=full_data[full_data['year_of_building']>2025].index
# full_data = full_data.drop(index=incorrect_year)


'''handling incorrect furniture'''
print(full_data['furniture'].value_counts())

'''handling incorrect house_type'''
print(full_data['house_type'].value_counts())


'''handling incorrect floor-number'''
full_data['Floor']=full_data['Floor'].astype(float)
full_data['Total_Floor']=full_data['Total_Floor'].astype(float)

incorrect_year_floor=full_data[full_data['Floor']<1].index
full_data = full_data.drop(index=incorrect_year_floor)
incorrect_year_floor=full_data[full_data['Floor']>30].index
full_data = full_data.drop(index=incorrect_year_floor)

incorrect_year_floor=full_data[full_data['Total_Floor']<1].index
full_data = full_data.drop(index=incorrect_year_floor)
incorrect_year_floor=full_data[full_data['Total_Floor']>30].index
full_data = full_data.drop(index=incorrect_year_floor)


full_data.drop(columns=['description'],inplace=True)
print(full_data.dtypes)
print(full_data.shape)
full_data.to_csv('../data/processed_data_nauryzbaiski.csv',index=False)

