import sys
import requests
import pandas
import simplejson as json
from datetime import datetime
from dateutil.relativedelta import relativedelta
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.palettes import Category20
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
today = datetime.today().strftime('%Y-%m-%d')
begin = datetime.strftime(datetime.today() + relativedelta(years=-1), '%Y-%m-%d')

@app.route('/')
def root():
    return redirect('/index')

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html', today=today, start=begin)

@app.route('/graph', methods=['GET','POST'])
def graph():
    if request.method == 'GET':
        return render_template('graph.html')
    else:
        ticker= request.form['ticker']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        form_open = ''
        adj_open = ''
        high = ''
        adj_high = ''
        low = ''
        adj_low = ''
        close = ''
        adj_close = ''
        
        api_url = '''https://www.quandl.com/api/v3/datasets/WIKI/%s/data.json?api_key=XxmSiACUars8yTcqLQhX&start_date=%s&end_date=%s''' % (ticker, start_date, end_date)
        session = requests.Session()
        session.mount('https://', requests.adapters.HTTPAdapter(max_retries=3))
        raw_data = session.get(api_url)

        raw_data = raw_data.json()
        ticker_df = pandas.DataFrame(raw_data['dataset_data']['data'], 
            columns=raw_data['dataset_data']['column_names'])
        ticker_df['Date'] = pandas.to_datetime(ticker_df['Date'])

        plot = figure(title='Data from Quandle for %s' % ticker,
              x_axis_label='date',
              x_axis_type='datetime')

        if request.form.get('open'):
            plot.line(x=ticker_df['Date'].values, 
                y=ticker_df['Open'].values,
                line_width=2, line_color=Category20[20][0], legend='Open')
            form_open = 'checked'
        if request.form.get('adj_open'):
            plot.line(x=ticker_df['Date'].values, 
                y=ticker_df['Adj. Open'].values,
                line_width=2, line_color=Category20[20][1], legend='Adj. Open')
            adj_open = 'checked'
        if request.form.get('high'):
            plot.line(x=ticker_df['Date'].values, 
                y=ticker_df['High'].values,
                line_width=2, line_color=Category20[20][2], legend='High')
            high = 'checked'
        if request.form.get('adj_high'):
            plot.line(x=ticker_df['Date'].values, 
                y=ticker_df['Adj. High'].values,
                line_width=2, line_color=Category20[20][3], legend='Adj. High')
            adj_high = 'checked'
        if request.form.get('low'):
            plot.line(x=ticker_df['Date'].values, 
                y=ticker_df['Low'].values,
                line_width=2, line_color=Category20[20][4], legend='Low')
            low = 'checked'
        if request.form.get('adj_low'):
            plot.line(x=ticker_df['Date'].values, 
                y=ticker_df['Adj. Low'].values,
                line_width=2, line_color=Category20[20][5], legend='Adj. Low')
            adj_low = 'checked'
        if request.form.get('close'):
            plot.line(x=ticker_df['Date'].values, 
                y=ticker_df['Close'].values,
                line_width=2, line_color=Category20[20][10], legend='Close')
            close = 'checked'
        if request.form.get('adj_close'):
            plot.line(x=ticker_df['Date'].values, 
                y=ticker_df['Adj. Close'].values,
                line_width=2, line_color=Category20[20][11], legend='Adj. Close')
            adj_close = 'checked'
        

        script, div = components(plot)
        return render_template('graph.html', ticker=ticker, 
            end=end_date, start=start_date, script=script, div=div,
            form_open=form_open, adj_open=adj_open, high=high, adj_high=adj_high,
            low=low, adj_low=adj_low, close=close, adj_close=adj_close)

if __name__ == '__main__':
    app.run(port=33507)

