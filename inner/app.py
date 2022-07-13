from flask import Flask, request, redirect, url_for, render_template
import requests
import json, os
import apikey as a

def create_app():
    app = Flask(__name__)
    headers = {
        'X-CMC_PRO_API_KEY': a.mykey,
        'Accepts': 'application/json'
    }
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

    @app.route('/', methods = ['POST', 'GET'])
    def root():
        if request.method == 'POST':
            start = request.form.get('search1')
            limit = request.form.get('search2')
            fiat = request.form.get('search3')
            screen = list()
            if start.isdigit():
                if limit.isdigit():
                    start = int(start)
                    limit = int(limit)
                    if abs(start - limit) <= 100:
                        if fiat.lower() in 'usd eur rup'.split():
                            fiat = fiat.upper()
                            params = {
                                'start': start,
                                'limit': limit,
                                'convert': fiat
                            }
                            try:
                                jsn = requests.get(url, params,
                                    headers = headers).json()
                                for i, coin in enumerate(jsn['data']):
                                    screen.append(str(i + 1) + ') ' + coin['symbol'] + ':'
                                    + str(coin['quote'][fiat]['price']))
                                return render_template('res.html', answer = '  '.join(screen),
                                                        rankrange = str(start) + '-' + str(limit))
                            except:
                                return render_template('base.html')
            return render_template('base.html')
        return render_template('base.html')
    return app