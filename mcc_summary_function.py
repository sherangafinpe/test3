def mcc_summary_def(all_data,month_value):

    df = all_data[all_data['Month'] == month_value]

    mcc_category_df = df[['MCC', 'MCC Category']]
    mcc_category_df = mcc_category_df.drop_duplicates()
    mcc_category_df = mcc_category_df.reset_index(drop=True)
    mcc_category_df['MCC'] = mcc_category_df['MCC'].astype(str)

    mcc_dict = {}

    mcc_dict['month'] = month_value
    mcc_dict['volume'] = f"{round(df['Transaction Amount LKR'].sum()/1000000000,2):,}"
    mcc_dict['net_income_loss_etc'] = f"{round(df['Net Income Profit/Loss in LKR (Excluding Terminal Costs)'].sum()/1000000,2):,}"
    mcc_dict['net_income_loss_itc'] = f"{round(df['Net Income Profit/Loss in LKR (Including Terminal Costs)'].sum()/1000000,2):,}"
    mcc_dict['mcc_count'] = f"{len(set(df['MCC'])):,}"
    mcc_dict['profitable_mid_count'] = f"{len((df['Merchant Name'][df['loss_income_status_itc'] == 'Profit'])):,}"
    mcc_dict['unprofitable_mid_count'] = f"{len((df['Merchant Name'][df['loss_income_status_itc'] == 'Loss'])):,}"
    mcc_dict['percentage_mid_count'] = str(round(100*len((df['Merchant Name'][df['loss_income_status_itc'] == 'Profit']))/(len((df['Merchant Name'][df['loss_income_status_itc'] == 'Profit'])) + len((df['Merchant Name'][df['loss_income_status_itc'] == 'Loss']))),2)) + '%'

    mcc_net_df = df.groupby(['MCC'])['Net Income Profit/Loss in LKR (Including Terminal Costs)'].agg(['sum']).reset_index()
    mcc_net_df.columns = ['MCC', 'Net Income Loss ITC']

    mcc_count_df = df.groupby(['MCC'])['Transaction Amount LKR'].agg(['sum','count']).reset_index()
    mcc_count_df.columns = ['MCC', 'Volume', 'Total Merchants']

    profitable_mcc_count_df = df[df['loss_income_status_itc'] == 'Profit']
    profitable_mcc_count_df = profitable_mcc_count_df.groupby('MCC')['Transaction Amount LKR'].agg(['count']).reset_index()
    profitable_mcc_count_df.columns = ['MCC', 'Total Profitable Merchants']

    unprofitable_mcc_count_df = df[df['loss_income_status_itc'] == 'Loss']
    unprofitable_mcc_count_df = unprofitable_mcc_count_df.groupby('MCC')['Transaction Amount LKR'].agg(['count']).reset_index()
    unprofitable_mcc_count_df.columns = ['MCC', 'Total Unprofitable Merchants']


    mcc_count_df = mcc_count_df.merge(mcc_net_df, on='MCC', how='left')
    mcc_count_df = mcc_count_df.merge(profitable_mcc_count_df, on='MCC', how='left')
    mcc_count_df = mcc_count_df.merge(unprofitable_mcc_count_df, on='MCC', how='left')
    mcc_count_df = mcc_count_df.fillna(0)

    mcc_count_df['Percentage of Profitable Merchants'] = round(100*mcc_count_df['Total Profitable Merchants']/mcc_count_df['Total Merchants'],2)
    mcc_count_df['Percentage of Profitable Merchants'] = mcc_count_df['Percentage of Profitable Merchants'].astype(str) + '%'

    mcc_count_df['MCC'] = mcc_count_df['MCC'].astype(str)
    mcc_count_df['Total Profitable Merchants'] = mcc_count_df['Total Profitable Merchants'].astype(int)
    mcc_count_df['Total Unprofitable Merchants'] = mcc_count_df['Total Unprofitable Merchants'].astype(int)
    mcc_count_df['Volume'] = round(mcc_count_df['Volume'],2).apply(lambda x : "{:,}".format(x))
    mcc_count_df['Net Income Loss ITC'] = round(mcc_count_df['Net Income Loss ITC'],2).apply(lambda x : "{:,}".format(x))

    mcc_count_df = mcc_count_df.merge(mcc_category_df, on='MCC', how='left')
    mcc_count_df = mcc_count_df[['MCC', 'MCC Category', 'Volume', 'Net Income Loss ITC', 'Total Merchants', 'Total Profitable Merchants','Total Unprofitable Merchants', 'Percentage of Profitable Merchants']]

    mcc_count_df.sort_values(by='Total Profitable Merchants', ascending=False, inplace=True)

    return mcc_count_df, mcc_dict
