from scholarships.models import Ronin

import datetime
import requests


def local_api(var):

    ronins = Ronin.objects.all().filter(owner=var)
    
    urls = []
    for ronin in ronins:
        url = 'https://game-api.axie.technology/api/v1/{}'.format(ronin)
        urls.append(url)

    api = []
    for url in urls:
        data = requests.get(url).json()
        last_claim = datetime.datetime.fromtimestamp(data['last_claim'])
        data['last_claim'] = last_claim
        api.append(data)

    return api


def currency():
    slp_usd = 'https://api.coingecko.com/api/v3/simple/price?ids=smooth-love-potion&vs_currencies=usd'
    slp_usd = requests.get(slp_usd).json()

    return slp_usd


