import datetime
import numpy as np
import pandas as pd
from jqdatasdk import *
auth('13361285504', 'FrX5Wv7eq8JrarHB')
from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/convertible-bond')
def convertible_bond():
    q1=query(bond.CONBOND_BASIC_INFO).filter(bond.CONBOND_BASIC_INFO.list_status_id == '301001')
    df1=bond.run_query(q1)
    
    # name=list(('code','债券代码'),('short_name','债券简称'),('full_name','债券全称'),('list_status_id','上市状态编码，见下表上市状态编码对照表'),('list_status','上市状态'),('issuer','发行人'),('company_code','发行人股票代码（带后缀）'),('issue_start_date','发行起始日'),('issue_end_date','发行终止日'),('plan_raise_fund','计划发行总量（万元）'),('actual_raise_fund','实际发行总量（万元）'),('issue_par','发行面值'),('issue_price','发行价格'),('is_guarantee','是否有担保(1-是，0-否）'),('fund_raising_purposes','募资用途说明'),('list_datelist_declare_date','上市公告日期'),('convert_price_reason','初始转股价确定方式'),('convert_price','初始转股价格'),('convert_start_date','转股开始日期'),('convert_end_date','转股终止日期'),('convert_code','转股代码（不带后缀）'),('coupon','初始票面利率'),('exchange_code','交易市场编码，见下表交易市场编码'),('exchange','交易市场'),('currency_id','货币代码。CNY-人民币'),('coupon_type_id','计息方式编码，见下表计息方式编码'),('coupon_type','计息方式'),('coupon_frequency','付息频率，单位：月/次。按年付息是12月/次；半年付息是6月/次'),('payment_type_id','兑付方式编码，见下表兑付方式编码表'),('payment_type','兑付方式'),('par'float'债券面值(元)'),('repayment_period','偿还期限(月）'),('bond_type_id','债券分类编码，见下表债券分类编码'),('bond_type','债券分类'),('bond_form_id','债券形式编码，见下表债券形式编码表'),('bond_form','债券形式'),('list_date','上市日期'),('delist_Date','退市日期'),('interest_begin_date','起息日'),('maturity_date','到期日'),('interest_date','付息日'),('last_cash_date','最终兑付日'),('cash_comment','兑付说明'))
    return render_template('convertible-bond.html', tables=[df1.to_html(classes='data', header="true")])

@app.route('/conbond')
def conbond(name=None):
    date='2022-01-06'
    bond=jq_conbond(date)
    return render_template('conbond.html', name=bond)

def jq_conbond(date=str(datetime.date.today())):
    q1=query(bond.CONBOND_BASIC_INFO).filter(bond.CONBOND_BASIC_INFO.list_status_id == '301001')
    q2=query(bond.CONBOND_DAILY_PRICE).filter(bond.CONBOND_DAILY_PRICE.date==date).order_by(bond.CONBOND_DAILY_PRICE.close.asc())
    q3=query(bond.CONBOND_CONVERT_PRICE_ADJUST)

    df1=bond.run_query(q1)
    df2=bond.run_query(q2)
    df3=bond.run_query(q3)
    # 可转债转股价格调整 转换日期倒序和去重
    df4=df3.sort_values(by=['adjust_date'], ascending=False).drop_duplicates(subset='code', keep='first')
    df=df2.merge(df1, on='code', how='left').merge(df4[['code', 'new_convert_price']],on='code',how='left')

    price_df=get_price(df['company_code'].dropna().tolist(), start_date=date, end_date=date)

    df=df.merge(price_df, left_on='company_code', right_on='code', how='left')

    df['conversion_value']=100/df['new_convert_price']*df['close_y']
    df['conversion_premium']=df['close_x']/df['conversion_value']-1
    df['remaining_days']=pd.to_datetime(df['convert_end_date']) - datetime.datetime.now()
    # 按转股溢价率升序排序
    complete=df.sort_values(by='conversion_premium')[['code_x','name','close_x','new_convert_price','close_y','convert_start_date','convert_end_date','delist_Date','conversion_value','conversion_premium','remaining_days']]
    return complete