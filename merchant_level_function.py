import pandas as pd


month_order = pd.read_csv('month_order.csv')

col = ['Month', 'Merchant Name',
       'Transaction Amount LKR', 'Transaction Count',
       'Net Income Profit/Loss in LKR (Excluding Terminal Costs)',
       'Net Income Profit/Loss in LKR (Including Terminal Costs)',
       'Terminal Costs',
       'Gross Commission LKR',
       'Total On-US Volume',
       'Total International Volume',
       'Net DCC Income LKR',
       'Scheme Costs',
       'new_interchange_cost_lkr',
       'Interchange Cost Rate',
       'Commission Rate',
       'On-us Penetration Rate (as a % of Overall volume) %',
       'International Transaction Amount as a % of Total Transaction Amount %',
       'Average Income Rate',
       'Average Cost (Excluding Terminal Cost)', 
       'Average Cost (Including Terminal Cost)',
       'dcc_penetration']

values_columns = ['Transaction Amount LKR', 'Transaction Count',
                   'Net Income Profit/Loss in LKR (Excluding Terminal Costs)',
                   'Net Income Profit/Loss in LKR (Including Terminal Costs)',
                   'Terminal Costs',
                   'Gross Commission LKR',
                   'Total On-US Volume',
                   'Total International Volume',
                   'Net DCC Income LKR',
                   'Scheme Costs',
                   'new_interchange_cost_lkr']

rate_columns = ['Interchange Cost Rate',
               'Commission Rate',
               'On-us Penetration Rate (as a % of Overall volume) %',
               'International Transaction Amount as a % of Total Transaction Amount %',
               'Average Income Rate',
               'Average Cost (Excluding Terminal Cost)', 
               'Average Cost (Including Terminal Cost)',
               'dcc_penetration']

merchant_name = ['KEELLS']

merchant_name = ['JETWING BEACH']

def merchant_level_def(all_data,merchant_name):
    
    if 'Select All' in merchant_name:
        df = all_data.copy()
    
    else:
        df = all_data[all_data['Merchant Name'].isin(merchant_name)]
       
    
    df['dcc_penetration'] = 100*df['Net DCC Income LKR']/df['Total International Volume']
    
    df = df[col]

    df = df.fillna(0)
    
    df_group = df.groupby(['Month', 'Merchant Name'])[col[2:]].sum().reset_index()
    
    df = df_group.copy()
    
    df['Interchange Cost Rate'] = 100*df['new_interchange_cost_lkr']/df['Transaction Amount LKR']
    
    df['Commission Rate'] = 100*df['Gross Commission LKR']/df['Transaction Amount LKR'] 
    
    df['On-us Penetration Rate (as a % of Overall volume) %'] = 100*df['Total On-US Volume']/df['Transaction Amount LKR'] 

    df['International Transaction Amount as a % of Total Transaction Amount %'] = 100*df['Total International Volume']/df['Transaction Amount LKR'] 

    df['Average Income Rate'] = (df['Gross Commission LKR'] + 100*df['Net DCC Income LKR'])/df['Transaction Amount LKR'] 

    df['Average Cost (Excluding Terminal Cost)'] = 100*(df['new_interchange_cost_lkr'] + df['Scheme Costs'])/df['Transaction Amount LKR']
    
    df['Average Cost (Including Terminal Cost)'] = 100*(df['new_interchange_cost_lkr'] + df['Scheme Costs'] + df['Terminal Costs'])/df['Transaction Amount LKR']
    
    df['dcc_penetration'] = 100*df['Net DCC Income LKR']/df['Total International Volume']
    
    
    df[values_columns] = df[values_columns].apply(lambda x: round(x, 2))
    
    new_df = pd.DataFrame()
    
    new_df = month_order.merge(df, on='Month', how='left')
    
    new_df = new_df.fillna(0)
    
    merchant_level_dict = {}
    
    for i in range(0,len(col[2:])):
        merchant_level_dict[col[2:][i]] = list(new_df[col[2:][i]])
    
    for i in range(0,len(values_columns)):
        df[values_columns[i]] =  round(df[values_columns[i]],2).apply(lambda x : "{:,}".format(x))
   
    
    df[rate_columns] = df[rate_columns]*1
    df[rate_columns] = df[rate_columns].apply(lambda x: round(x, 4))
    df[rate_columns] = df[rate_columns].astype(str) + '%'

# =============================================================================
#     df.columns = ['Month', 'MCC', 'MCC Category', 'Merchant Name', 'volume', 'Transactions', 'Net Income/Loss ETC',
#                   'Net Income/Loss ITC', 'Terminal Cost', 'Interchange Cost', 'Interchange Cost Rate', 
#                   'Commission Rate', 'OnUs Penetration', 'Cross Border Penetration', 'Income Rate',
#                   'Cost Rate ETC', 'Cost Rate ITC', 'DCC Penetration']
# =============================================================================
    
    df1 = df.T
    df1 = df1.reset_index(drop=False)
    
    df1.columns = df1.iloc[0]
    df1 = df1[1:]

    df1.rename(columns = {0 : 'Index'}, inplace=True)

    print(df1)

    return df1, merchant_level_dict