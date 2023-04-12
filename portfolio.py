from flask import Flask, render_template, request  # Importing the render_template function from Flask module to render HTML templates.
import sys
sys.path.append('/home/sj/code/quant/economic-data-tools/eastmoney')
from eastmoney import F10

app = Flask(__name__)

@app.route('/portfolio')
def portfolio():
    code=request.args.get('code', default='SH600161')
    date=request.args.get('date', default='2022-03-31')
    a=F10()
    b=a.shareholder_research(code=code, date=date)
    # holders = b['sjkzr'][0]['HOLDER_NAME']
    return render_template('stock.html', holders=b['sjkzr'][0])  # This code returns a template named 'stock.html' which can be used to display stock information.
