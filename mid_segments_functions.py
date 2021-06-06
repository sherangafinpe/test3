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

def mid_segment_kpi_values(all_data, month_value, mcc_value_list, volume_type_value_list, normal):
    
    df = all_data[all_data['Month'] == month_value]

    if 'Select All' in mcc_value_list:
        df = df.copy()

        if 'Select All' not in volume_type_value_list:
            df = df[df['VOLUME_TYPE_ITC'].isin(volume_type_value_list)]

    
    else:
        if 'Select All' in volume_type_value_list:
            df = df[df['MCC'].isin(mcc_value_list)]
        
        else:
            df = df[df['MCC'].isin(mcc_value_list)]
            df = df[df['VOLUME_TYPE_ITC'].isin(volume_type_value_list)]

    df = df.fillna(0)
    
    mid_segment_dict = {}

    mid_segment_dict['month'] = month_value
    mid_segment_dict['MCC'] = mcc_value_list
    mid_segment_dict['volume_type'] = volume_type_value_list
    
    mid_segment_dict['total_merchants'] =  f"{round(len((df['Merchant Name'])),2):,}"

    value, string_value = million_or_billion(df['Transaction Amount LKR'].sum(), normal)
    mid_segment_dict['volume'] = f"{round(df['Transaction Amount LKR'].sum()/value,2):,}" +  string_value
    
    mid_segment_dict['total_trxn_count'] = f"{round(df['Transaction Count'].sum(),2):,}"

    value, string_value = million_or_billion(df['Net Income Profit/Loss in LKR (Excluding Terminal Costs)'].sum(), normal)
    mid_segment_dict['net_income_loss_etc'] = f"{round(df['Net Income Profit/Loss in LKR (Excluding Terminal Costs)'].sum()/value,2):,}" + string_value
    
    value, string_value = million_or_billion(df['Net Income Profit/Loss in LKR (Including Terminal Costs)'].sum(), normal)
    mid_segment_dict['net_income_loss_itc'] = f"{round(df['Net Income Profit/Loss in LKR (Including Terminal Costs)'].sum()/value,2):,}"  + string_value
    
    

    value, string_value = million_or_billion(df['Terminal Costs'].sum(), normal)
    mid_segment_dict['terminal_cost'] = f"{round(df['Terminal Costs'].sum()/value,2):,}" + string_value
    
    mid_segment_dict['commision_rate'] = str(round(100*df['Gross Commission LKR'].sum()/df['Transaction Amount LKR'].sum(),2)) + '%'
    
    value, string_value = million_or_billion(df['Interchange Cost LKR'].sum(), normal)
    mid_segment_dict['interchange_cost'] = f"{round(df['Interchange Cost LKR'].sum()/1000000,2):,}" + string_value
    
    mid_segment_dict['average_interchange_rate'] = str(round(100*df['Interchange Cost LKR'].sum()/df['Transaction Amount LKR'].sum(),2)) + '%'
    
    mid_segment_dict['onus_penetration_rate_domestic_volume'] = str(round(100*df['Total On-US Volume'].sum()/df['Total Domestic Volume'].sum(),2)) + '%'
    
    mid_segment_dict['cross_border_penetration_rate'] = str(round(100*df['Total International Volume'].sum()/df['Transaction Amount LKR'].sum(),2)) + '%'
    
    mid_segment_dict['average_income_rate'] = str(round(100*(df['Gross Commission LKR'].sum() + df['Customer Recovery Fuel Amount'].sum() + df['Net DCC Income LKR'].sum() + df['terminal_income'].sum())/df['Transaction Amount LKR'].sum(),2)) + '%'
    
    mid_segment_dict['average_costs_etc'] = str(round(100*(df['Interchange Cost LKR'].sum() + df['Scheme Costs'].sum())/df['Transaction Amount LKR'].sum(),2)) + '%'
    
    mid_segment_dict['average_costs_itc'] = str(round(100*(df['Interchange Cost LKR'].sum() + df['Scheme Costs'].sum() + df['Terminal Costs'].sum())/df['Transaction Amount LKR'].sum(),2)) + '%'
    
    mid_segment_dict['dcc_penetration'] = str(round(100*df['dcc_volume'].sum()/df['Total International Volume'].sum(),2)) + '%'

    return mid_segment_dict


def mid_segments_def(all_data, month_value, mcc_value_list, volume_type_value_list):

    month_df = all_data[all_data['Month'] == month_value]
    
    if 'Select All' in mcc_value_list:
        df = month_df.copy()

        if 'Select All' not in volume_type_value_list:
            df = df[df['VOLUME_TYPE_ITC'].isin(volume_type_value_list)]

    
    else:
        if 'Select All' in volume_type_value_list:
            df = month_df[month_df['MCC'].isin(mcc_value_list)]
        
        else:
            df = month_df[month_df['MCC'].isin(mcc_value_list)]
            df = df[df['VOLUME_TYPE_ITC'].isin(volume_type_value_list)]

    df = df.fillna(0)
    
    mid_segment_dict = mid_segment_kpi_values(all_data, month_value, mcc_value_list, volume_type_value_list, normal=True)
    
    month_lists = ['January', 'July', 'November']
    
    graph_list = []
    for m in range(0,len(month_lists)):
        
        graph_list.append(mid_segment_kpi_values(all_data, month_lists[m], mcc_value_list, volume_type_value_list, normal=False))
        
    graph_df = pd.DataFrame(graph_list)
    
    required_kpi = ['total_merchants', 'volume',
       'total_trxn_count', 'net_income_loss_etc', 'net_income_loss_itc',
       'terminal_cost', 'commision_rate', 'interchange_cost',
       'average_interchange_rate', 'onus_penetration_rate_domestic_volume',
       'cross_border_penetration_rate', 'average_income_rate',
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
        

    
    return df, mid_segment_dict, kpi_dict