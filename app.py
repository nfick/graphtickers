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

        api_url = '''https://www.quandl.com/api/v3/datasets/WIKI/%s/data.json?
             api_key=XxmSiACUars8yTcqLQhX&
             start_date=%s&end_date=%s''' % (ticker, start_date, end_date)
        session = requests.Session()
        session.mount('https://', requests.adapters.HTTPAdapter(max_retries=3))
        raw_data = session.get(api_url)

        data = raw_data.json()
        ticker_df = pandas.DataFrame(data['data'], columns=data['column_names'])
        ticker_df ['Date'] = pandas.to_datetime(ticker_df ['Date'])

        plot = figure(tools=TOOLS,
              title='Data from Quandle for %s' % ticker,
              x_axis_label='date',
              x_axis_type='datetime')

        if request.form.get('Open'):
            plot.line(x=ticker_df['Date'].values, 
                y=ticker_df['Open'].values,
                line_width=2, line_color=Category20[20][0], legend='Open')
        if request.form.get('Adj. Open'):
            plot.line(x=ticker_df['Date'].values, 
                y=ticker_df['Adj. Open'].values,
                line_width=2, line_color=Category20[20][1], legend='Adj. Open')
         if request.form.get('High'):
            plot.line(x=ticker_df['Date'].values, 
                y=ticker_df['High'].values,
                line_width=2, line_color=Category20[20][2], legend='High')
        if request.form.get('Adj. High'):
            plot.line(x=ticker_df['Date'].values, 
                y=ticker_df['Adj. High'].values,
                line_width=2, line_color=Category20[20][3], legend='Adj. High')
        if request.form.get('Low'):
            plot.line(x=ticker_df['Date'].values, 
                y=ticker_df['Low'].values,
                line_width=2, line_color=Category20[20][4], legend='Low')
        if request.form.get('Adj. Low'):
            plot.line(x=ticker_df['Date'].values, 
                y=ticker_df['Adj. Low'].values,
                line_width=2, line_color=Category20[20][5], legend='Adj. Low')
        if request.form.get('Close'):
            plot.line(x=ticker_df['Date'].values, 
                y=ticker_df['Close'].values,
                line_width=2, line_color=Category20[20][6], legend='Close')
        if request.form.get('Adj. Close'):
            plot.line(x=ticker_df['Date'].values, 
                y=ticker_df['Adj. Close'].values,
                line_width=2, line_color=Category20[20][7], legend='Adj. Close')
        

        script, div = components(plot)
        return render_template('graph.html', end=end_date, start=start_date,
                               script=script, div=div)

if __name__ == '__main__':
    app.run(port=33507)

