"""
Created on Tue May 17 22:45:18 2020

@author: Maya Bohora
"""

import pandas as pd

# Defining global variables
path = './input/itcont_2020_20010425_20190426.txt'
path_out = './output/results.txt'
#Percentile
percentile = .3

data = pd.read_csv(path, sep="|", header=None)

#Inserting columns'name.
data.columns = ["CMTE_ID", "AMNDT_IND",	"RPT_TP","TRANSACTION_PGI", "IMAGE_NUM", "TRANSACTION_TP", "ENTITY_TP", "NAME",	"CITY", "STATE", "ZIP_CODE", "EMPLOYER", "OCCUPATION", "TRANSACTION_DT", "TRANSACTION_AMT", "OTHER_ID", "TRAN_ID", "FILE_NUM", "MEMO_CD", "MEMO_TEXT", "SUB_ID"]


#Building new dataframe that consists the following columns.
df = data[['CMTE_ID','NAME','ZIP_CODE','TRANSACTION_DT','TRANSACTION_AMT','OTHER_ID']]

#Removing all the rows which consists less or greather five ZIP_CODE digits.
df = df.loc[df['ZIP_CODE'].astype('str').str.len() == 5]

#Removing all the rows with less than zero transaction amount. 
df = df.loc[df['TRANSACTION_AMT'] >= 0]

#Extracting last four digit year from TRANSACTION_DT
def extract_char(x):
    x = str(x)
    four_char = x[-4:]
    return four_char

df['YEAR'] = df['TRANSACTION_DT'].apply(extract_char)

#Removing the rows with null values.
df = df.dropna(subset=['CMTE_ID','NAME','ZIP_CODE','TRANSACTION_DT','TRANSACTION_AMT'])
df.shape

#Removing rows with no null values in OTHER_ID.
df = df[df['OTHER_ID'].isnull()]

#Creating data frame named df_results to calculate total contribution, total count and percentile value for the repeated donor.
df_results = df.groupby(['CMTE_ID','ZIP_CODE','YEAR'])['TRANSACTION_AMT']\
              .agg({'TOTAL_CON': 'sum',"COUNT": 'size'})\
              .join(df.groupby(['CMTE_ID','ZIP_CODE','YEAR'])['TRANSACTION_AMT']\
              .quantile(percentile)).reset_index()

#Creating data frame to order the columns
df_results_ordered = df_results[['CMTE_ID', 'ZIP_CODE', 'YEAR','TRANSACTION_AMT', 'TOTAL_CON', 'COUNT']]

#Writing data frame to the output folder.
df_results_ordered.to_csv(path_out, sep="|", header=None, index=False)







