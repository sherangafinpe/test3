
import pandas as pd


def million_or_billion(value,normal=False):

    if normal==True:
        million = 1000000
        billion = 1000000000
        if abs(value/million) <1:
            return 1, ''
        elif abs(value/billion) >=1:
            return billion, ' Billion'
        else:
            return million, " Million"

    else:
        return 1, ""


def kpi_values(df, month_value, mcc_value_list, normal):
        
        df = df[df['Month'] == month_value]
        
        unprofitable_dict = {}
    
        unprofitable_dict['month'] = month_value
        unprofitable_dict['MCC'] = mcc_value_list

        if "Select All" not in mcc_value_list:
            df = df[df['MCC'].isin(mcc_value_list)]
        
        unprofitable_dict['unprofitable_mid_count'] = f"{len((df['Merchant Name'][df['loss_income_status_itc'] == 'Loss'])):,}"
    
        unprofitable_dict['percentage_mid_count'] = str(round(100*len((df['Merchant Name'][df['loss_income_status_itc'] == 'Loss']))/df.shape[0],2)) + '%'

        value, string_value = million_or_billion(df['Transaction Amount LKR'][df['loss_income_status_itc'] == 'Loss'].sum(),normal)
        unprofitable_dict['volume'] =  f"{round(df['Transaction Amount LKR'][df['loss_income_status_itc'] == 'Loss'].sum()/value,2):,}" +  string_value
        
        
        value, string_value = million_or_billion(df['Net Income Profit/Loss in LKR (Excluding Terminal Costs)'][df['loss_income_status_itc'] == 'Loss'].sum(),normal)
        unprofitable_dict['net_income_loss_etc'] = f"{round(df['Net Income Profit/Loss in LKR (Excluding Terminal Costs)'][df['loss_income_status_itc'] == 'Loss'].sum()/value,2):,}" +  string_value
        
        value, string_value = million_or_billion(df['Net Income Profit/Loss in LKR (Including Terminal Costs)'][df['loss_income_status_itc'] == 'Loss'].sum(),normal)
        unprofitable_dict['net_income_loss_itc'] = f"{round(df['Net Income Profit/Loss in LKR (Including Terminal Costs)'][df['loss_income_status_itc'] == 'Loss'].sum()/value,2):,}" +  string_value
        
        unprofitable_dict['on-us_pentraion_overall_domestic'] = str(round(100*(df['Total On-US Volume'][df['loss_income_status_itc'] == 'Loss'].sum())/df['Total Domestic Volume'][df['loss_income_status_itc'] == 'Loss'].sum(),2)) + "%"
        
        unprofitable_dict['cross_border_overall_volume'] = str(round(100*(df['Transaction Amount LKR'][df['loss_income_status_itc'] == 'Loss'].sum() - df['Total Domestic Volume'][df['loss_income_status_itc'] == 'Loss'].sum())/df['Transaction Amount LKR'][df['loss_income_status_itc'] == 'Loss'].sum(),2)) + "%"
        
        value, string_value = million_or_billion(df['Terminal Costs'][df['loss_income_status_itc'] == 'Loss'].sum(),normal)
        unprofitable_dict['terminal_cost'] = f"{round(df['Terminal Costs'][df['loss_income_status_itc'] == 'Loss'].sum()/value,2):,}" +  string_value
        
        unprofitable_dict['commision_rate'] = str(round(100*df['Gross Commission LKR'][df['loss_income_status_itc'] == 'Loss'].sum()/df['Transaction Amount LKR'][df['loss_income_status_itc'] == 'Loss'].sum(),2)) + '%'
        
        value, string_value = million_or_billion(df['Interchange Cost LKR'][df['loss_income_status_itc'] == 'Loss'].sum(),normal)
        unprofitable_dict['interchange_cost'] = f"{round(df['Interchange Cost LKR'][df['loss_income_status_itc'] == 'Loss'].sum()/value,2):,}" +  string_value
        
        unprofitable_dict['average_interchange_rate'] = str(round(100*df['Interchange Cost LKR'][df['loss_income_status_itc'] == 'Loss'].sum()/df['Transaction Amount LKR'][df['loss_income_status_itc'] == 'Loss'].sum(),2)) + '%'
    
        unprofitable_dict['average_income_rate'] = str(round(100*(df['Gross Commission LKR'][df['loss_income_status_itc'] == 'Loss'].sum() + df['terminal_income'][df['loss_income_status_itc'] == 'Loss'].sum()  + df['Customer Recovery Fuel Amount'][df['loss_income_status_itc'] == 'Loss'].sum() + df['Net DCC Income LKR'][df['loss_income_status_itc'] == 'Loss'].sum())/df['Transaction Amount LKR'][df['loss_income_status_itc'] == 'Loss'].sum(),2)) + '%'
        
        unprofitable_dict['average_costs_etc'] = str(round(100*(df['Interchange Cost LKR'][df['loss_income_status_itc'] == 'Loss'].sum() + df['Scheme Costs'][df['loss_income_status_itc'] == 'Loss'].sum())/df['Transaction Amount LKR'][df['loss_income_status_itc'] == 'Loss'].sum(),2)) + '%'
        
        unprofitable_dict['average_costs_itc'] = str(round(100*(df['Interchange Cost LKR'][df['loss_income_status_itc'] == 'Loss'].sum() + df['Scheme Costs'][df['loss_income_status_itc'] == 'Loss'].sum() + df['Terminal Costs'][df['loss_income_status_itc'] == 'Loss'].sum())/df['Transaction Amount LKR'][df['loss_income_status_itc'] == 'Loss'].sum(),2)) + '%'
        
        unprofitable_dict['dcc_penetration'] = str(round(100*df['dcc_volume'][df['loss_income_status_itc'] == 'Loss'].sum()/df['Total International Volume'][df['loss_income_status_itc'] == 'Loss'].sum(),2)) + '%'
      
        unprofitable_dict['dcc_volume'] = f"{round(df['dcc_volume'][df['loss_income_status_itc'] == 'Loss'].sum()/1000000,2):,}"

        return unprofitable_dict



def unprofitable_merchants_def(all_data, month_value, mcc_value_list):
    
    col_list = ['Month', 'MCC', 'MCC Category', 'Merchant Name',
       'Transaction Amount LKR', 'Transaction Count',
       'Net Income Profit/Loss in LKR (Excluding Terminal Costs)',
       'Net Income Profit/Loss in LKR (Including Terminal Costs)',
       'On-us Penetration Rate (as a % of Overall volume) %',
       'On-us Penetration Rate (as a % of Overall domestic volume)%',
       'Domestic Transaction Amount as a % of Total Transaction Amount %',
       'International Transaction Amount as a % of Total Transaction Amount %',
       'Total On-US Volume', 'Total Domestic Volume',
       'Total International Volume', 
       'Gross Commission LKR',
       'Commission Rate', 'Net DCC Income LKR', 'DCC Income Rate',
       'Customer Recovery Fuel Amount', 
       'Interchange Cost LKR',
       'Interchange Cost LKR (Excluding On-Us)', 
       'Customer Recovery Fuel Amount Rate',
       'Extra Costs', 'Number of Terminals', 'Terminal Costs', 'Scheme Costs',
       'Interchange Cost Rate', 'Interchange Cost Rate (Excluding On-Us)',
       'Other Costs', 'Average Scheme Costs',
       'Average Cost (Including Terminal Cost)',
       'Average Cost (Excluding Terminal Cost)', 'Average Income Rate',
       'Average Margin (Including Terminal Costs)',
       'Average Margin (Excluding Terminal Costs)',
       'Profit Margin (Including Terminal Costs)',
       'Profit Margin (Excluding Terminal Costs)',
       'Net Income loss (Excluding Terminal Costs)- Excluding on-us',
       'Net Income loss (Including Terminal Costs)- Excluding on-us',
       'Average Cost (Including Terminal Cost) - Excluding On-Us Interchange Rate',
       'Average Cost (Excluding Terminal Cost) - Excluding On-Us Interchange Rate',
       'Average Margin (Including Terminal Costs) - Excluding On-us',
       'Average Margin (Excluding Terminal Costs)- Excluding On-us',
       'average_interchange_rate', 'average_interchange_rate_ex_onus',
       'average_income_rate_dcc_commission_rate',
       'average_cost_etc_ex_onus_interchange_rate']
    

    unprofitable_df = pd.DataFrame()
    unprofitable_dict = {}
    kpi_dict = {}


    month_df = all_data[all_data['Month'] == month_value]

    print(month_df.shape[0])

    if month_df.shape[0]!=0:
    
        if 'Select All' in mcc_value_list:
            df = month_df.copy()
            
        
        else:
            df = month_df[month_df['MCC'].isin(mcc_value_list)]
        
        df = df.fillna(0)
        
        print(month_df.shape[0])
        
        unprofitable_dict = kpi_values(all_data, month_value, mcc_value_list, normal=True)
        
        month_lists = ['January_2020', 'July_2020', 'November_2020', 'December_2020', 'January_2021', 'February_2021']
        
        graph_list = []
        for m in range(0,len(month_lists)):
            
            graph_list.append(kpi_values(all_data, month_lists[m], mcc_value_list, normal=False))
            
        
        graph_df = pd.DataFrame(graph_list)
        
        required_kpi = ['unprofitable_mid_count', 'percentage_mid_count', 'volume', 'net_income_loss_etc', 
                        'net_income_loss_itc', 'on-us_pentraion_overall_domestic', 'cross_border_overall_volume', 
                        'terminal_cost', 'commision_rate', 'interchange_cost', 'average_interchange_rate', 'average_income_rate',
                        'average_costs_etc', 'average_costs_itc', 'dcc_penetration']
        
        kpi_dict = {}
        
        
        for i in range(0,len(required_kpi)):
            
            if "%" in str(graph_df.loc[0,required_kpi[i]]):
                kpi_list = ",".join(list(map(str,list(graph_df[required_kpi[i]].str.rstrip("%")))))
            elif "," in str(graph_df.loc[0,required_kpi[i]]):
                kpi_list = list(graph_df[required_kpi[i]])
                kpi_list = [ j.replace(",","") for j in kpi_list]
                kpi_list = ','.join(kpi_list)
            else:
                kpi_list = ",".join(list(map(str,list(graph_df[required_kpi[i]]))))
                
            kpi_dict[required_kpi[i]] = kpi_list
            
        
        unprofitable_df = df[df['loss_income_status_itc'] == 'Loss']
        
        unprofitable_df = unprofitable_df[col_list]
        
        unprofitable_df['MCC'] = unprofitable_df['MCC'].astype(str)
        

        thousand_seperator_col = ['Transaction Amount LKR', 'Transaction Count',
            'Net Income Profit/Loss in LKR (Excluding Terminal Costs)',
        'Net Income Profit/Loss in LKR (Including Terminal Costs)',
        'Total On-US Volume', 'Total Domestic Volume',
        'Total International Volume', 
        'Gross Commission LKR',
        'Net DCC Income LKR', 
        'Customer Recovery Fuel Amount', 
        'Interchange Cost LKR',
        'Interchange Cost LKR (Excluding On-Us)', 
        'Customer Recovery Fuel Amount Rate',
        'Extra Costs', 'Number of Terminals', 'Terminal Costs', 'Scheme Costs'
        ]


        percentage_col = ['On-us Penetration Rate (as a % of Overall volume) %',
        'On-us Penetration Rate (as a % of Overall domestic volume)%',
        'Domestic Transaction Amount as a % of Total Transaction Amount %',
        'International Transaction Amount as a % of Total Transaction Amount %',
        'Commission Rate', 'DCC Income Rate',
        'Customer Recovery Fuel Amount Rate',
        'Interchange Cost Rate', 'Interchange Cost Rate (Excluding On-Us)',
        'Other Costs', 'Average Scheme Costs',
        'Average Cost (Including Terminal Cost)',
        'Average Cost (Excluding Terminal Cost)', 'Average Income Rate',
        'Average Margin (Including Terminal Costs)',
        'Average Margin (Excluding Terminal Costs)',
        'Profit Margin (Including Terminal Costs)',
        'Profit Margin (Excluding Terminal Costs)',
        'Net Income loss (Excluding Terminal Costs)- Excluding on-us',
        'Net Income loss (Including Terminal Costs)- Excluding on-us',
        'Average Cost (Including Terminal Cost) - Excluding On-Us Interchange Rate',
        'Average Cost (Excluding Terminal Cost) - Excluding On-Us Interchange Rate',
        'Average Margin (Including Terminal Costs) - Excluding On-us',
        'Average Margin (Excluding Terminal Costs)- Excluding On-us',
        'average_interchange_rate', 'average_interchange_rate_ex_onus',
        'average_income_rate_dcc_commission_rate',
        'average_cost_etc_ex_onus_interchange_rate']

        
        for k in range(0,len(thousand_seperator_col)):
            print(k)
            unprofitable_df[thousand_seperator_col[k]] = unprofitable_df[thousand_seperator_col[k]].apply(lambda x : "{:,}".format(x))
        
        unprofitable_df[percentage_col] = unprofitable_df[percentage_col].astype(str) + '%'


    #unprofitable_df['Transaction Amount LKR'] = unprofitable_df['Transaction Amount LKR'].apply(lambda x : "{:,}".format(x))
    
    return unprofitable_df, unprofitable_dict, kpi_dict
