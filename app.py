from flask import Flask, render_template, request  # Importing the render_template function from Flask module to render HTML templates.
from eastmoney.f10 import shareholder_research

app = Flask(__name__)

@app.route('/sjkzr')
def sjkzr():
    """Render the stock.html template with shareholder research data.

    Args:
        code (str): The stock code.
        date (str): The date of the shareholder research.

    Returns:
        str: The rendered HTML template with shareholder research data.
    """
    code=request.args.get('code', default='SH600161')
    date=request.args.get('date', default='2022-03-31')
    b=shareholder_research(code=code, date=date)
    # holders = b['sjkzr'][0]['HOLDER_NAME']
    return render_template('stock.html', holders=b['sjkzr'][0])
