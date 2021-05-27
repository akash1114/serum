from django.shortcuts import render
import requests
import cryptocompare
from datetime import datetime


# Create your views here.
def home(request):
    data = get_data()
    return render(request, 'home.html', {'output': data})


def get_data():
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    data = requests.get('https://api.lunarcrush.com/v2?data=market-pairs&key=wus9gkvfjvh6zp9nry1c7w&symbol=SRM',
                        params={'headers': header, 'limit': 200})
    tokens = []
    pairs = []
    i = 0
    for pair in data.json()['data'][0]['marketPairs']:
        new_pair = {}
        if pair['from_symbol'] not in tokens:
            tokens.append(pair['from_symbol'])
        if pair['to_symbol'] not in tokens:
            tokens.append(pair['to_symbol'])
        new_pair['token0'] = pair['from_symbol']
        new_pair['token1'] = pair['to_symbol']
        new_pair['Update'] = pair['last_updated']
        pairs.append(new_pair)

    tokens = list(filter(None, tokens))
    coin_details = cryptocompare.get_coin_list(format=False)
    coin_price = cryptocompare.get_price(tokens, currency='USD')
    data = []
    for pair in pairs:
        try:
            token0 = {'url': coin_details[pair['token0']]['Url'], 'symbol': pair['token0'],
                                                      'name': coin_details[pair['token0']]['CoinName']}
            token0Price = coin_price[pair['token0']]['USD']
        except:
            token0 = {'id': '-', 'symbol': pair['token0'],'name': pair['token0']}
            token0Price = '-'

        try:
            token1 = {'url': coin_details[pair['token1']]['Url'], 'symbol': pair['token1'],
                      'name': coin_details[pair['token1']]['CoinName']}
            token1Price = coin_price[pair['token1']]['USD']
        except:
            token1 = {'id': '-', 'symbol': pair['token1'], 'name': pair['token1']}
            token1Price = '-'

        try:
            updated = datetime.fromtimestamp(int(pair['Update']))
        except:
            updated = 'None'
        single_pair = {'index': i + 1, 'token0': token0,
                       'token1': token1,
                       'token0Price': token0Price,
                       'token1Price': token1Price,
                       'updated':updated}

        data.append(single_pair)
        i += 1
    return data


