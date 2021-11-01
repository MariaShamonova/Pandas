# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    data = pd.read_csv('https://raw.githubusercontent.com/justmarkham/DAT8/master/data/chipotle.tsv', sep='\t')
    pd.options.display.max_columns = None
    # pd.options.display.max_colwidth = None
    temp = data['choice_description'].head(20)
    
    number_observerations = len(data.index)
    all_columns = data.columns
    most_common_values = data['item_name'].mode().values

  
    print("Number of observations: ",number_observerations)
    print('Columns: ', ', '.join(list(data.columns)))
    print("Most common values: ",  ', '.join(most_common_values))
    
    data_frequency = data['item_name'].value_counts()
    data_frequency.plot(kind='bar', figsize=(95,30), fontsize=100)  