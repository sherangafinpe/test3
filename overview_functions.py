def overview_def(all_data,month_value):

    df = all_data[all_data['Month'] == month_value]
    
    overview_dict = {}

    overview_dict['month'] = month_value
    overview_dict['total_merchants'] =  f"{round(len((df['Merchant Name'])),2):,}"
    
    overview_dict['volume'] = f"{round(df['Transaction Amount LKR'].sum()/1000000000,2):,}"
    
    overview_dict['total_trxn_count'] = f"{round(df['Transaction Count'].sum(),2):,}"
    overview_dict['net_income_loss_etc'] = f"{round(df['Net Income Profit/Loss in LKR (Excluding Terminal Costs)'].sum()/1000000,2):,}"
    overview_dict['net_income_loss_itc'] = f"{round(df['Net Income Profit/Loss in LKR (Including Terminal Costs)'].sum()/1000000,2):,}"
    
    
    overview_dict['terminal_cost'] = f"{round(df['Terminal Costs'].sum()/1000000,2):,}"
    
    overview_dict['commision_rate'] = str(round(100*df['Gross Commission LKR'].sum()/df['Transaction Amount LKR'].sum(),2)) + '%'
    
    overview_dict['interchange_cost'] = f"{round(df['Interchange Cost LKR'].sum()/1000000,2):,}"
    
    overview_dict['average_interchange_rate'] = str(round(100*df['Interchange Cost LKR'].sum()/df['Transaction Amount LKR'].sum(),2)) + '%'
    
    overview_dict['onus_penetration_rate_domestic_volume'] = str(round(100*df['Total On-US Volume'].sum()/df['Total Domestic Volume'].sum(),2)) + '%'
    
    overview_dict['cross_border_penetration_rate'] = str(round(100*df['Total International Volume'].sum()/df['Transaction Amount LKR'].sum(),2)) + '%'
    
    overview_dict['average_income_rate'] = str(round(100*(df['Gross Commission LKR'].sum() + df['Customer Recovery Fuel Amount'].sum() + df['Net DCC Income LKR'].sum() + df['terminal_income'].sum())/df['Transaction Amount LKR'].sum(),3)) + '%'
    
    
    overview_dict['average_costs_etc'] = str(round(100*(df['Interchange Cost LKR'].sum() + df['Scheme Costs'].sum())/df['Transaction Amount LKR'].sum(),3)) + '%'
    
    overview_dict['average_costs_itc'] = str(round(100*(df['Interchange Cost LKR'].sum() + df['Scheme Costs'].sum() + df['Terminal Costs'].sum())/df['Transaction Amount LKR'].sum(),3)) + '%'
    
    overview_dict['dcc_volume'] = f"{round(df['dcc_volume'].sum()/1000000,2):,}"

    overview_dict['dcc_penetration'] = str(round(100*df['dcc_volume'].sum()/df['Total International Volume'].sum(),2)) + '%'

    return overview_dict
