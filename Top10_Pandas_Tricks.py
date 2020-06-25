# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

url = 'https://en.wikipedia.org/wiki/Table_of_food_nutrients'

'''
1. Web tables scraping using read_html(match)
'''
## OPTION 1: Read in all the tables
all_foods_tables = pd.read_html(url)
print(f'** Total data tables = {len(all_foods_tables)} **')
## ** Total data tables = 16 **

### return a list of individual data frame
dairy_table = all_foods_tables[0]
print(dairy_table.head())

## OPTION 2: using the arg. match 
dairy_table = pd.read_html(url, match='Fortified milk')

dairy_table = dairy_table[0]
print(dairy_table.head())

'''
** Total data tables = 16 **
                       0        1    ...       7         8
0         Dairy products      NaN    ...     NaN       NaN
1                   Food  Measure    ...     Fat  Sat. fat
..                   ...      ...    ...     ...       ...
3                   skim    1 qt.    ...       t         t
4   Buttermilk, cultured    1 cup    ...       5         4
'''


'''
2. Config options at interpreter/IDE startup
'''
pd.get_option('display.max_columns')
pd.get_option('display.max_rows')

def start_config():
    options = {
        'display': {
            'max_columns': None,    ### Max # of columns
            'max_colwidth': 1000,   ### Max width of columns
            'max_rows': 1000,       ### Max # of rows 
            'precision': 3          ### Float number precision
        }
    }

    for display, optionVals in options.items():
        for setting, userVal in optionVals.items():
            pd.set_option(f'{display}.{setting}', userVal)  

if __name__ == '__main__':
    start_config()
    del start_config    ### Clean up the namespace


## Here, we take a subset of the entire table for demonstration purpose
dairy_table_raw = dairy_table.iloc[1:23, ]
dairy_table_raw.columns = dairy_table_raw[:1].iloc[0]
dairy_table_raw = dairy_table_raw[1:].reset_index(drop=True)

dairy_table = dairy_table_raw.iloc[:, :4]


"""
3. Use itertuples() to loop through each row 
"""
### df.itertuples()
for row in dairy_table.itertuples():
    if row[0] == 0:
        print(f'{row}')
        break
# Pandas(Index=0, Food="Cows' milk, whole", Measure='1 qt.', Grams='976', Calories='660')
  
dairy_table = dairy_table_raw.iloc[:, :4]
      
cur_str = ''    
missing_value_row = 0
for row in dairy_table.itertuples():    
    idx = row[0]
    
    if str(row.Measure)=='nan':
        cur_str += f'{row.Food} '
        missing_value_row = idx  
        
    if cur_str and idx == missing_value_row+1:
        cur_str += row.Food
        dairy_table.iloc[idx, 0] = cur_str
        cur_str = ''
        
dairy_table = dairy_table.dropna(how='any') 


'''
4. fillna(method) 
use shift() to compare rows, where 
    shift(-1): shift to the next row; 
    shift(1): shift to the previous row
'''

dairy_table = dairy_table.fillna(method='bfill') 
original_cols = dairy_table.columns


'''
5. Work with Bolleans with cumsum()
'''
keys = (dairy_table != dairy_table.shift(1)).iloc[:, 1:].astype(int).cumsum()
### string in python: vectorized operation; same pattern 
keys.columns = keys.columns + '_'
dairy_table = pd.concat([dairy_table, keys], axis=1)


'''
6. Introspect the GroupBy object
'''
new_food_col = dairy_table.groupby(['Measure_', 'Grams_', 'Calories_'], as_index=False)['Food'].apply(' '.join).reset_index(drop=True) 

dairy_table = dairy_table.drop(columns='Food').drop_duplicates().reset_index(drop=True)
dairy_table.insert(0, column='Food', value=new_food_col)
dairy_table = dairy_table[original_cols]

#### groups and get_group to introspect the groupby object 
dairy_table_groupby = dairy_table.groupby(['Measure_', 'Grams_', 'Calories_'], as_index=False)

for k in dairy_table_groupby.groups.keys():
    print(f'{"="*80}')
    print(dairy_table_groupby.get_group(k))

'''
to be continued...
'''




