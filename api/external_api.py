from scholarships.models import Ronin

import datetime
import requests


def external_api(var):

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


# fecth schplarship name absent in api
def external_api2(var):

    ronins = Ronin.objects.all().filter(owner=var).values_list('ronin', flat=True)
    ronins_0x = [ronin.replace('ronin:', '0x') for ronin in ronins]

    urls = []
    for ronin in ronins_0x:
        url = 'https://graphql-gateway.axieinfinity.com/graphql?query={publicProfileWithRoninAddress(roninAddress:"%s"){name}}' % ronin
        urls.append(url)

    api2 = []
    for url in urls:
        data = requests.get(url).json()
        api2.append(data)
    
    return api2


def currency():
    slp_usd = 'https://api.coingecko.com/api/v3/simple/price?ids=smooth-love-potion&vs_currencies=usd'
    slp_usd = requests.get(slp_usd).json()

    return slp_usd


