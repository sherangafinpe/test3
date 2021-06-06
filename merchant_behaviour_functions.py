# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 07:30:01 2021

@author: Sheranga
"""



import pandas as pd
import numpy as np


def percentage_change(x,y):
    if (x!=0) & (y!=0):
        return np.round(100*(y-x)/x,2)

def merchant_status(x,y):
    
    if x==0:
        return 'New Merchant'
    elif y==0:
        return 'Dropped Merchant'
    elif x-y>0:
        return 'Volume Decreased'
    elif y-x>=0:
        return 'Volume Increased'
    else:
        return 'Other'

def merchant_behavior_def(all_data):


    r_col = ['Month','Merchant Name',
            'Transaction Amount LKR', 
            'Transaction Count', 
            'Net Income Profit/Loss in LKR (Excluding Terminal Costs)',
            'Net Income Profit/Loss in LKR (Including Terminal Costs)', 
            'On-us Penetration Rate (as a % of Overall volume) %',
            'On-us Penetration Rate (as a % of Overall domestic volume)%',
            'International Transaction Amount as a % of Total Transaction Amount %',
            'Total On-US Volume',
            'Total Domestic Volume',
            'Total International Volume',
            'Gross Commission LKR',
            'Commission Rate',
            'Net DCC Income LKR']



    df = all_data.copy()

    # df = df[df['Month'] != 'January']
    
    latest_month_list = ['January_2021', 'February_2021']
    
    df = df[df['Month'].isin(latest_month_list)]
    
    df = df[r_col]
    
    df_group = df.groupby(['Month', 'Merchant Name'])[r_col[2:]].sum().reset_index()
    
    
    df_previous = df_group[df_group['Month']==latest_month_list[0]]
    
    df_latest = df_group[df_group['Month']==latest_month_list[-1]]
    
    dropped_merchants = list(set(df_previous['Merchant Name']) - set(df_latest['Merchant Name']))
    
    new_merchants = list(set(df_latest['Merchant Name']) - set(df_previous['Merchant Name']))
    
    
    new_df = df[df['Merchant Name'].isin(new_merchants)]
    new_df['Merchant Status'] = 'New Merchant'
    
    dropped_df = df[df['Merchant Name'].isin(dropped_merchants)]
    dropped_df['Merchant Status'] = 'Dropped Merchant'
    
    pivot_df = pd.DataFrame()
    
    pivot_df = pivot_df.append(new_df, ignore_index=True)
    
    
    pivot_df = pivot_df.append(dropped_df, ignore_index=True)
    
    pivot_df['On-us Penetration Rate (as a % of Overall volume) %'] = 100*pivot_df['Total On-US Volume']/pivot_df['Transaction Amount LKR'] 
    
    pivot_df['On-us Penetration Rate (as a % of Overall domestic volume)%'] = 100*pivot_df['Total On-US Volume']/pivot_df['Total Domestic Volume'] 
    
    pivot_df['International Transaction Amount as a % of Total Transaction Amount %'] = 100*pivot_df['Total International Volume']/pivot_df['Transaction Amount LKR'] 
    
    pivot_df['Commission Rate'] = 100*pivot_df['Gross Commission LKR']/pivot_df['Transaction Amount LKR'] 
    
    
    pivot_df['On-us Penetration Rate (as a % of Overall volume) %'] = round(pivot_df['On-us Penetration Rate (as a % of Overall volume) %'],3)
    pivot_df['On-us Penetration Rate (as a % of Overall domestic volume)%'] = round(pivot_df['On-us Penetration Rate (as a % of Overall domestic volume)%'],3)
    pivot_df['International Transaction Amount as a % of Total Transaction Amount %'] = round(pivot_df['International Transaction Amount as a % of Total Transaction Amount %'],3)
    pivot_df['Commission Rate'] = round(pivot_df['Commission Rate'],3)
    
    
    pivot_df['On-us Penetration Rate (as a % of Overall volume) %'] = pivot_df['On-us Penetration Rate (as a % of Overall volume) %'].astype(str) + '%'

    pivot_df['On-us Penetration Rate (as a % of Overall domestic volume)%'] = pivot_df['On-us Penetration Rate (as a % of Overall domestic volume)%'].astype(str) + '%'
    
    pivot_df['International Transaction Amount as a % of Total Transaction Amount %'] = pivot_df['International Transaction Amount as a % of Total Transaction Amount %'].astype(str) + '%'
    
    pivot_df['Commission Rate'] = pivot_df['Commission Rate'].astype(str) + '%'
    
    
    pivot_df['Transaction Amount LKR'] = round(pivot_df['Transaction Amount LKR'],2).apply(lambda x : "{:,}".format(x))
    
    pivot_df['Transaction Count'] = round(pivot_df['Transaction Count'],2).apply(lambda x : "{:,}".format(x))
    
    pivot_df['Net Income Profit/Loss in LKR (Excluding Terminal Costs)'] = round(pivot_df['Net Income Profit/Loss in LKR (Excluding Terminal Costs)'],2).apply(lambda x : "{:,}".format(x))
    
    pivot_df['Net DCC Income LKR'] = round(pivot_df['Net DCC Income LKR'],2).apply(lambda x : "{:,}".format(x))
    
    pivot_df['Total On-US Volume'] = round(pivot_df['Total On-US Volume'],2).apply(lambda x : "{:,}".format(x))
    
    pivot_df['Total Domestic Volume'] = round(pivot_df['Total Domestic Volume'],2).apply(lambda x : "{:,}".format(x))
    
    pivot_df['Total International Volume'] = round(pivot_df['Total International Volume'],2).apply(lambda x : "{:,}".format(x))
    
    pivot_df['Gross Commission LKR'] = round(pivot_df['Gross Commission LKR'],2).apply(lambda x : "{:,}".format(x))
    
        

# =============================================================================
#     df['MCC'] = df['MCC'].astype(str)
#     df[r_col[1:4]] = df[r_col[1:4]].apply(lambda x: x.str.strip())
# 
#     pivot_df = df.pivot_table(index=r_col[1:4] , columns=["Month"], values=r_col[4:]).reset_index()
# 
# 
#     pivot_df.columns =r_col[1:4] + [s1 + '_' + str(s2) for (s1,s2) in pivot_df.columns.tolist()[3:]]
#     pivot_df = pivot_df.fillna(0)
# 
#     pivot_df['Percentage Changes'] = pivot_df.apply(lambda z: percentage_change(z['Transaction Amount LKR_January_2021'], z['Transaction Amount LKR_February_2021']), axis=1)
#     pivot_df['Merchant Status'] = pivot_df.apply(lambda z: merchant_status(z['Transaction Amount LKR_January_2021'], z['Transaction Amount LKR_February_2021']), axis=1)
# 
# 
#     pivot_df = pivot_df[['MCC', 'MCC Category', 'Merchant Name',
#                         'Transaction Amount LKR_January_2021', 'Transaction Amount LKR_February_2021',
#         'Transaction Count_January_2021', 'Transaction Count_February_2021',
#         'Net Income Profit/Loss in LKR (Excluding Terminal Costs)_January_2021',
#         'Net Income Profit/Loss in LKR (Excluding Terminal Costs)_February_2021',
#         'Net Income Profit/Loss in LKR (Including Terminal Costs)_January_2021',
#         'Net Income Profit/Loss in LKR (Including Terminal Costs)_February_2021',
#         'Net DCC Income LKR_January_2021',
#         'Net DCC Income LKR_February_2021',
#         'On-us Penetration Rate (as a % of Overall volume) %_January_2021',
#         'On-us Penetration Rate (as a % of Overall volume) %_February_2021',
#         'On-us Penetration Rate (as a % of Overall domestic volume)%_January_2021',
#         'On-us Penetration Rate (as a % of Overall domestic volume)%_February_2021',
#         'International Transaction Amount as a % of Total Transaction Amount %_January_2021', 'International Transaction Amount as a % of Total Transaction Amount %_February_2021',
#         'Total On-US Volume_January_2021', 'Total On-US Volume_February_2021',
#         'Total Domestic Volume_January_2021', 'Total Domestic Volume_February_2021',
#         'Total International Volume_January_2021', 'Total International Volume_February_2021',
#         'Gross Commission LKR_January_2021', 'Gross Commission LKR_February_2021',
#         'Commission Rate_January_2021', 'Commission Rate_February_2021', 'Percentage Changes',
#         'Merchant Status']]
# 
# 
#     pivot_df['On-us Penetration Rate (as a % of Overall volume) %_January_2021'] = pivot_df['On-us Penetration Rate (as a % of Overall volume) %_January_2021'].astype(str) + '%'
#     pivot_df['On-us Penetration Rate (as a % of Overall volume) %_February_2021'] = pivot_df['On-us Penetration Rate (as a % of Overall volume) %_February_2021'].astype(str) + '%'
# 
#     pivot_df['On-us Penetration Rate (as a % of Overall domestic volume)%_January_2021'] = pivot_df['On-us Penetration Rate (as a % of Overall domestic volume)%_January_2021'].astype(str) + '%'
#     pivot_df['On-us Penetration Rate (as a % of Overall domestic volume)%_February_2021'] = pivot_df['On-us Penetration Rate (as a % of Overall domestic volume)%_February_2021'].astype(str) + '%'
# 
#     pivot_df['International Transaction Amount as a % of Total Transaction Amount %_January_2021'] = pivot_df['International Transaction Amount as a % of Total Transaction Amount %_January_2021'].astype(str) + '%'
#     pivot_df['International Transaction Amount as a % of Total Transaction Amount %_February_2021'] = pivot_df['International Transaction Amount as a % of Total Transaction Amount %_February_2021'].astype(str) + '%'
# 
#     pivot_df['Commission Rate_January_2021'] = pivot_df['Commission Rate_January_2021'].astype(str) + '%'
#     pivot_df['Commission Rate_February_2021'] = pivot_df['Commission Rate_February_2021'].astype(str) + '%'
# 
# 
# 
# 
#     pivot_df['Transaction Amount LKR_January_2021'] = round(pivot_df['Transaction Amount LKR_January_2021'],2).apply(lambda x : "{:,}".format(x))
#     pivot_df['Transaction Amount LKR_February_2021'] = round(pivot_df['Transaction Amount LKR_February_2021'],2).apply(lambda x : "{:,}".format(x))
# 
#     pivot_df['Transaction Count_January_2021'] = round(pivot_df['Transaction Count_January_2021'],2).apply(lambda x : "{:,}".format(x))
#     pivot_df['Transaction Count_February_2021'] = round(pivot_df['Transaction Count_February_2021'],2).apply(lambda x : "{:,}".format(x))
# 
#     pivot_df['Net Income Profit/Loss in LKR (Excluding Terminal Costs)_January_2021'] = round(pivot_df['Net Income Profit/Loss in LKR (Excluding Terminal Costs)_January_2021'],2).apply(lambda x : "{:,}".format(x))
#     pivot_df['Net Income Profit/Loss in LKR (Excluding Terminal Costs)_February_2021'] = round(pivot_df['Net Income Profit/Loss in LKR (Excluding Terminal Costs)_February_2021'],2).apply(lambda x : "{:,}".format(x))
# 
#     pivot_df['Net DCC Income LKR_January_2021'] = round(pivot_df['Net DCC Income LKR_January_2021'],2).apply(lambda x : "{:,}".format(x))
#     pivot_df['Net DCC Income LKR_February_2021'] = round(pivot_df['Net DCC Income LKR_February_2021'],2).apply(lambda x : "{:,}".format(x))
# 
#     pivot_df['Total On-US Volume_January_2021'] = round(pivot_df['Total On-US Volume_January_2021'],2).apply(lambda x : "{:,}".format(x))
#     pivot_df['Total On-US Volume_February_2021'] = round(pivot_df['Total On-US Volume_February_2021'],2).apply(lambda x : "{:,}".format(x))
# 
#     pivot_df['Total Domestic Volume_January_2021'] = round(pivot_df['Total Domestic Volume_January_2021'],2).apply(lambda x : "{:,}".format(x))
#     pivot_df['Total Domestic Volume_February_2021'] = round(pivot_df['Total Domestic Volume_February_2021'],2).apply(lambda x : "{:,}".format(x))
# 
#     pivot_df['Total International Volume_January_2021'] = round(pivot_df['Total International Volume_January_2021'],2).apply(lambda x : "{:,}".format(x))
#     pivot_df['Total International Volume_February_2021'] = round(pivot_df['Total International Volume_February_2021'],2).apply(lambda x : "{:,}".format(x))
# 
#     pivot_df['Gross Commission LKR_January_2021'] = round(pivot_df['Gross Commission LKR_January_2021'],2).apply(lambda x : "{:,}".format(x))
#     pivot_df['Gross Commission LKR_February_2021'] = round(pivot_df['Gross Commission LKR_February_2021'],2).apply(lambda x : "{:,}".format(x))
# 
# 
# =============================================================================

    return pivot_df



