from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd
import numpy as np

import mcc_summary_function
import unprofitable_merchants_functions
import overview_functions
import mid_segments_functions
import plotly_test
import merchant_behaviour_functions
import profitable_merchants_functions
import merchant_level_function

import plotly_test
import json

app = Flask(__name__)

mid_level_data = pd.read_csv('merchant_level_v8.csv',encoding='cp1252')
mid_level_data['MCC'] = mid_level_data['MCC'].astype(str)

mcc_category_df = pd.read_csv("MCC Category.csv", encoding='cp1252')
mcc_category_df = mcc_category_df.sort_values(by='MCC')
mcc_category_df['MCC'] = mcc_category_df['MCC'].astype(str)

#new_df = pd.read_csv('merchant_behavior_v2.csv',encoding='cp1252')
#new_df.loc[new_df['Merchant Name'] == '0', 'Merchant Name'] = 'BLANK'

new_dropped_merchant_df = pd.read_csv('new_dropped_merchants.csv',encoding='cp1252')

month_list = list(set(mid_level_data['Month']))

merchant_list = list(set(mid_level_data['Merchant Name']))
merchant_list.sort()


@app.route('/test', methods=['GET', 'POST'])
def test():
    graphJSON = plotly_test.plotly_global_timeseries()
    print(graphJSON)

    x = "100.1,59.47,80.00,81.11,56.67,55.45,40.88,20.45,40.98,80.66,88.34,61.01"
    return render_template("test.html", graphJSON=graphJSON, title='Test123',x=x)

@app.route('/test2', methods=['GET', 'POST'])
def test1():
    labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    return render_template("test2.html", labels=labels)


@app.route('/login', methods=['GET', 'POST'])
def login():

    
    if request.method == "POST":
        username = str(request.form.get('email-address'))
        password = str(request.form.get('password'))

        print(username)
        print(password)

        if (username == "sheranga@finpe.co.uk") & (password == "test"):
            return redirect(url_for("index"))
        else:
            return redirect(url_for("login"))
    else:
        return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return redirect(url_for("login"))

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    kpi_dict = {}
    kpi_dict['total_merchants'] = "7114,6099,6116,5964,5993,6099"
    kpi_dict['volume'] = "20.11,15.51,12.49,18.78,15.26,14.1"
    kpi_dict['transactions'] = "5178279,5170755,4436450,5733723,5209707,4868467"
    kpi_dict['net_etc'] = "12.83,44.04,33.92,47.96,40.86,36.06"
    kpi_dict['net_itc'] = "-3.52,28.68,19.05,31.68,24.63,19.77"
    kpi_dict['terminal_cost'] = "18.98,18.72,18.96,19.73,19.64,19.36"
    kpi_dict['interchange_cost'] = "286.34,208.78,167.47,255.64,204.5,190.42"
    kpi_dict['interchange_rate'] = "1.42,1.35,1.34,1.36,1.34,1.35"
    kpi_dict['commision_rate'] = "1.74,1.65,1.65,1.66,1.65,1.65"
    kpi_dict['onus_penetration'] = "11.08,10.93,10.55,10.66,10.37,10.65"
    kpi_dict['cross_border'] = "29.48,3.01,3.65,2.98,3.03,3.86"
    kpi_dict['dcc_volume'] = "209.04,3.21,1.49,4.43,5.71,6.72"
    kpi_dict['dcc'] = "3.53,0.69,0.33,0.79,1.23,1.23"
    kpi_dict['income_rate'] = "1.899,1.77,1.773,1.76,1.763,1.767"
    kpi_dict['cost_rate_etc'] = "1.844,1.495,1.498,1.512,1.505,1.522"
    kpi_dict['cost_rate_itc'] = "1.938,1.617,1.6651,1.617,1.634,1.659"


    labels = ['January-2020', 'July-2020', 'November-2020', 'December-2020', 'January-2021', 'February-2021']

    if request.method== 'GET':
        template_dict ={}
        month_value='February_2021'

    elif request.method == 'POST':
        month_value = str(request.form.get('dropdown1'))
        print(month_value)

    overview_dict = overview_functions.overview_def(mid_level_data,month_value)
    graphJSON = plotly_test.plotly_global_timeseries()
    graphJSON1 = plotly_test.plotly_net_income_loss()

    return render_template('index.html', 
                            month_list=month_list,
                            overview_dict=overview_dict,
                            graphJSON=graphJSON, 
                            graphJSON1=graphJSON1,
                            title='Test123',
                            labels=labels,
                            kpi_dict=kpi_dict,
                            month_value=month_value)


@app.route('/mcc_summary', methods=['GET', 'POST'])
def mcc_summary():

    results = []

    kpi_dict = {}

    kpi_dict['volume'] = "20.11,15.51,12.49,18.78,15.26,14.1"
    kpi_dict['net_etc'] = "12.83,44.04,33.92,48.43,40.56,35.77"
    kpi_dict['net_itc'] = "-3.47,28.55,18.88,32.04,24.03,19.51"
    kpi_dict['mcc_count'] = "175,170,158,164,168,165"
    kpi_dict['profitable_merchants'] = "5203,4819,4206,4588,4455,4329"
    kpi_dict['unprofitable_merchants'] = "1733,1172,1191,1132,1204,1335"
    kpi_dict['profitable_percentage'] = "75.01,80.44,77.93,80.21,78.72,76.43"


    if request.method== 'GET':
        month_value='February_2021'
        mcc_count_df, mcc_dict = mcc_summary_function.mcc_summary_def(mid_level_data,month_value)

    elif request.method == 'POST':
        month_value = str(request.form.get('dropdown1'))
        print(month_value)
        mcc_count_df, mcc_dict = mcc_summary_function.mcc_summary_def(mid_level_data,month_value)


    results = mcc_count_df.to_dict(orient='records')
    fieldnames = [key for key in results[0].keys()]

    return render_template('mcc_summary.html', 
                            results=results, 
                            fieldnames=fieldnames, 
                            len=len,
                            month_list=month_list,
                            mcc_dict=mcc_dict,
                            kpi_dict=kpi_dict,
                            month_value=month_value)


@app.route('/merchant_level', methods=['GET', 'POST'])
def merchant_level():

    results = []
    merchant_level_dict = {}

    if request.method== 'GET':
        merchant_value_list=['GEETHIKA HARDWARE & WELAD']
        merchant_value_selected_list = ['GEETHIKA HARDWARE & WELAD']
        merchant_level_df,merchant_level_dict = merchant_level_function.merchant_level_def(mid_level_data,merchant_value_list)

    elif request.method == 'POST':
        merchant_value_list = request.form.getlist('mcc_list[]')
        merchant_value_selected_list = request.form.getlist('mcc_list[]')
        print(merchant_value_list)
        merchant_level_df, merchant_level_dict = merchant_level_function.merchant_level_def(mid_level_data,merchant_value_list)


    results = merchant_level_df.head(50).to_dict(orient='records')
    fieldnames = [key for key in results[0].keys()]

    merchant_sub_list = merchant_list

    if request.method== 'GET':
        merchant_sub_list=merchant_sub_list
    if request.method == 'POST':
        if request.form.getlist('mcc_list[]') == ['Select All']:
            merchant_sub_list = list(set(merchant_sub_list) - set(request.form.getlist('mcc_list[]')))
            print("post")
        elif request.form.getlist('mcc_list[]') != ['Select All']:
            merchant_sub_list = list(set(merchant_sub_list) - set(request.form.getlist('mcc_list[]')))
            print("get")

    
    print(merchant_level_dict)

    return render_template('merchant_level.html', 
                            results=results, 
                            fieldnames=fieldnames, 
                            len=len,
                            merchant_list=merchant_sub_list,
                            merchant_value=merchant_value_list,
                            merchant_level_dict=merchant_level_dict)





@app.route('/profitable_merchants', methods=['GET', 'POST'])
def profitable_merchants():
    
    results = []
    profitable_dict = {}

    kpi_dict = {}

    if request.method== 'GET':
        month_value='February_2021'
        mcc_value_list = ['Select All']
        mcc_value_selected_list = ['Select All']

        profitable_df, profitable_dict, kpi_dict = profitable_merchants_functions.profitable_merchants_def(mid_level_data,month_value, mcc_value_list)

    elif request.method == 'POST':
        month_value = str(request.form.get('dropdown1'))
        mcc_value_list = request.form.getlist('mcc_list[]')
        mcc_value_selected_list = request.form.getlist('mcc_list[]')
        mcc_value_list = [mc.split(':-', 1)[0] for mc in mcc_value_list]
        print(month_value)
        print(mcc_value_list)
        profitable_df, profitable_dict, kpi_dict = profitable_merchants_functions.profitable_merchants_def(mid_level_data,month_value, mcc_value_list)
        print(request.form.getlist('mcc_list[]'))

    mcc_list = list(set(mid_level_data['MCC'][(mid_level_data['loss_income_status_itc']=='Profit') & (mid_level_data['Month'] == month_value)]))

    mcc_list =  list(mcc_category_df['Dropdown Name'][mcc_category_df['MCC'].isin(mcc_list)])

    if request.method== 'GET':
        mcc_list=mcc_list
    if request.method == 'POST':
        if request.form.getlist('mcc_list[]') == ['Select All']:
            mcc_list = list(set(mcc_list) - set(request.form.getlist('mcc_list[]')))
            print("post")
        elif request.form.getlist('mcc_list[]') != ['Select All']:
            mcc_list = ['Select All'] + list(set(mcc_list) - set(request.form.getlist('mcc_list[]')))
            print("get")


    


    #unprofitable_df = unprofitable_df.head(100)

    results = profitable_df.head(100).to_dict(orient='records')
    fieldnames = [key for key in results[0].keys()]

    #print(kpi_dict)
    return render_template('profitable_merchants.html', 
                            results=results, 
                            fieldnames=fieldnames, 
                            len=len,
                            month_list=month_list,
                            mcc_list=mcc_list,
                            profitable_dict=profitable_dict,
                            kpi_dict=kpi_dict,
                            month_value=month_value,
                            mcc_value_list=mcc_value_selected_list)

@app.route('/unprofitable_merchants', methods=['GET', 'POST'])
def unprofitable_merchants():
    
    results = []
    unprofitable_dict = {}

    kpi_dict = {}

    if request.method== 'GET':
        month_value='February_2021'
        mcc_value_list = ['Select All']
        mcc_value_selected_list = ['Select All']

        unprofitable_df, unprofitable_dict, kpi_dict = unprofitable_merchants_functions.unprofitable_merchants_def(mid_level_data,month_value, mcc_value_list)

    elif request.method == 'POST':
        month_value = str(request.form.get('dropdown1'))
        mcc_value_list = request.form.getlist('mcc_list[]')
        mcc_value_selected_list = request.form.getlist('mcc_list[]')
        mcc_value_list = [mc.split(':-', 1)[0] for mc in mcc_value_list]
        print(month_value)
        print(mcc_value_list)
        unprofitable_df, unprofitable_dict, kpi_dict = unprofitable_merchants_functions.unprofitable_merchants_def(mid_level_data,month_value, mcc_value_list)
        print(request.form.getlist('mcc_list[]'))

    mcc_list = list(set(mid_level_data['MCC'][(mid_level_data['loss_income_status_etc']=='Loss') & (mid_level_data['Month'] == month_value)]))

    mcc_list =  list(mcc_category_df['Dropdown Name'][mcc_category_df['MCC'].isin(mcc_list)])

    if request.method== 'GET':
        mcc_list=mcc_list
    if request.method == 'POST':
        if request.form.getlist('mcc_list[]') == ['Select All']:
            mcc_list = list(set(mcc_list) - set(request.form.getlist('mcc_list[]')))
            print("post")
        elif request.form.getlist('mcc_list[]') != ['Select All']:
            mcc_list = ['Select All'] + list(set(mcc_list) - set(request.form.getlist('mcc_list[]')))
            print("get")


    


    #unprofitable_df = unprofitable_df.head(100)

    results = unprofitable_df.to_dict(orient='records')
    fieldnames = [key for key in results[0].keys()]

    #print(kpi_dict)
    return render_template('unprofitable_merchants.html', 
                            results=results, 
                            fieldnames=fieldnames, 
                            len=len,
                            month_list=month_list,
                            mcc_list=mcc_list,
                            unprofitable_dict=unprofitable_dict,
                            kpi_dict=kpi_dict,
                            month_value=month_value,
                            mcc_value_list=mcc_value_selected_list)


@app.route('/merchant_behaviour', methods=['GET', 'POST'])
def merchant_behaviour():

    new_df = merchant_behaviour_functions.merchant_behavior_def(mid_level_data)

    new_merchants_df = new_df[new_df['Merchant Status'] == 'New Merchant']
    new_merchants_df = new_merchants_df.sort_values(by='Transaction Amount LKR', ascending=False)
    
    print(new_merchants_df)

    #new_merchants_df = new_merchants_df.head(100)
    dropped_merchants_df = new_df[new_df['Merchant Status'] == 'Dropped Merchant']
    dropped_merchants_df = dropped_merchants_df.sort_values(by='Transaction Amount LKR', ascending=False)
    
    print(dropped_merchants_df)
    #dropped_merchants_df = dropped_merchants_df.head(100)

    new_results = new_merchants_df.to_dict(orient='records')
    
    print(new_results)
    new_fieldnames = [key for key in new_results[0].keys()]

    dropped_results = dropped_merchants_df.to_dict(orient='records')
    dropped_fieldnames = [key for key in dropped_results[0].keys()]

    new_dropped_results = new_dropped_merchant_df.to_dict(orient='records')
    new_dropped_fieldnames = [key for key in new_dropped_results[0].keys()]

    mcc_dict = {}
    
    return render_template('merchant_behaviour.html',
                            mcc_dict=mcc_dict,
                            new_results=new_results,
                            new_fieldnames=new_fieldnames,
                            dropped_results=dropped_results,
                            dropped_fieldnames=dropped_fieldnames,
                            new_dropped_results=new_dropped_results,
                            new_dropped_fieldnames=new_dropped_fieldnames,
                            len=len)


@app.route('/mid_segments', methods=['GET', 'POST'])
def mid_segments():

    results = []
    mcc_list = list(set(mid_level_data['MCC']))
    mcc_list = ['Select All'] + list(mcc_category_df['Dropdown Name'][mcc_category_df['MCC'].isin(mcc_list)])
    volume_type_list = ['Select All'] + list(set(mid_level_data['VOLUME_TYPE_ITC']))

    ugly_blob=''

    kpi_dict = {}

    if request.method== 'GET':

        month_value='February_2021'

        mcc_value_list = ['Select All']
        mcc_value_selected_list = ['Select All']

        volume_type_value_list = ['LOW']
        volume_type_value_selected_list = ['LOW']


    elif request.method== 'POST':

        month_value = str(request.form.get('dropdown1'))
        mcc_value_list = request.form.getlist('mcc_list[]')
        mcc_value_selected_list = request.form.getlist('mcc_list[]')
        mcc_value_list = [mc.split(':-', 1)[0] for mc in mcc_value_list]
        
        volume_type_value_list = request.form.getlist('volume_type_value[]')
        volume_type_selected_list = request.form.getlist('volume_type_value[]')

    mid_segment_df, mid_segment_dict, kpi_dict = mid_segments_functions.mid_segments_def(mid_level_data, month_value, mcc_value_list, volume_type_value_list)

    mcc_list = list(set(mid_level_data['MCC']))
    mcc_list =  list(mcc_category_df['Dropdown Name'][mcc_category_df['MCC'].isin(mcc_list)])

    volume_type_list = ['Select All'] + list(set(mid_level_data['VOLUME_TYPE_ITC']))

    if request.method== 'GET':
        mcc_list=mcc_list
        volume_type_list = list(set(volume_type_list) - set(volume_type_value_list))
    if request.method == 'POST':

        volume_type_list = list(set(volume_type_list) - set(request.form.getlist('volume_type_value[]')))
        #if request.form.getlist('volume_type_value[]') == ['Select All']:
            

        if request.form.getlist('mcc_list[]') == ['Select All']:
            mcc_list = list(set(mcc_list) - set(request.form.getlist('mcc_list[]')))
            print("post")
        elif request.form.getlist('mcc_list[]') != ['Select All']:
            mcc_list = ['Select All'] + list(set(mcc_list) - set(request.form.getlist('mcc_list[]')))
            print("get")


    #mid_segment_df['Commission Rate'] = mid_segment_df['Commission Rate']

    results = mid_segment_df.head(1000).to_dict(orient='records')
    fieldnames = [key for key in results[0].keys()]

    mid_segment_df = mid_segment_df[mid_segment_df['Commission Rate']<=5]

    #mid_segment_df = mid_segment_df.head(10)

    percentile_list = [10,25,50,75,90]
    percentile_value = []
    for i in range(0,len(percentile_list)):            
        percentile_value.append(np.percentile(list(mid_segment_df['Transaction Count']),percentile_list[i]))

    mid_segment_df['size'] = 0
    mid_segment_df.loc[mid_segment_df['Transaction Count'] < percentile_value[0], 'size'] = 1
    mid_segment_df.loc[(mid_segment_df['Transaction Count'] >= percentile_value[0]) & (mid_segment_df['Transaction Count'] <= percentile_value[1]) , 'size'] = 3
    mid_segment_df.loc[(mid_segment_df['Transaction Count'] >= percentile_value[1]) & (mid_segment_df['Transaction Count'] <= percentile_value[2]) , 'size'] = 5
    mid_segment_df.loc[(mid_segment_df['Transaction Count'] >= percentile_value[2]) & (mid_segment_df['Transaction Count'] <= percentile_value[3]) , 'size'] = 7
    mid_segment_df.loc[(mid_segment_df['Transaction Count'] >= percentile_value[3]) & (mid_segment_df['Transaction Count'] <= percentile_value[4]) , 'size'] = 9
    mid_segment_df.loc[mid_segment_df['Transaction Count'] > percentile_value[4], 'size'] = 15

    profit_df = mid_segment_df[mid_segment_df['loss_income_status_itc'] == 'Profit']

    pr_commision_rate = list(profit_df['Commission Rate'])
    pr_volume = list(profit_df['Transaction Amount LKR'])
    pr_transactions = (list(profit_df['size']))
    pr_labels =  list(profit_df['Merchant Name'])

    #print(labels)
    
    pr_newlist = []
    for cr, v, t in zip(pr_commision_rate, pr_volume, pr_transactions):
        pr_newlist.append({'x': cr, 'y': v, 'r': t})

    
    loss_df = mid_segment_df[mid_segment_df['loss_income_status_itc'] == 'Loss']

    lo_commision_rate = list(loss_df['Commission Rate'])
    lo_volume = list(loss_df['Transaction Amount LKR'])
    lo_transactions = (list(loss_df['size']))
    lo_labels =  list(loss_df['Merchant Name'])

    #print(labels)
    
    lo_newlist = []
    for cr, v, t in zip(lo_commision_rate, lo_volume, lo_transactions):
        lo_newlist.append({'x': cr, 'y': v, 'r': t})


    labels = lo_labels + pr_labels

    
    
    #y_constant_value = [{'x': round(mid_segment_df['Commission Rate'].min(),1), 'y' : round(mid_segment_df['Transaction Amount LKR'].mean() + 1000)},
    #{'x': round(mid_segment_df['Commission Rate'].max() + 0.2,1), 'y' : round(mid_segment_df['Transaction Amount LKR'].mean() + 1000)}]

    #x_constant_value = [{'x': round(mid_segment_df['Commission Rate'].mean()), 'y' : 0},
    #{'x': round(mid_segment_df['Commission Rate'].mean()), 'y' : round(mid_segment_df['Transaction Amount LKR'].max() + 1000)}]


    


    
    pr_list = str(pr_newlist).replace('\'', '')
    lo_list = str(lo_newlist).replace('\'', '')

    #print(ugly_blob)

    #print(str(y_constant_value).replace('\'', ''))

    #print(str(x_constant_value).replace('\'', ''))

    #print(len(commision_rate))


    print(kpi_dict)
    return render_template('mid_segments.html', 
                            volume_type_list=volume_type_list, 
                            month_list=month_list,
                            mcc_list=mcc_list,
                            pr_data=pr_list,
                            lo_data=lo_list,
                            labels=labels,
                            transactions=pr_transactions,
                            mid_segment_dict=mid_segment_dict,
                            results=results,
                            fieldnames=fieldnames,
                            len=len,
                            kpi_dict=kpi_dict,
                            month_value=month_value,
                            mcc_value_list=mcc_value_selected_list,
                            volume_type_value_list=volume_type_value_list
                            )


