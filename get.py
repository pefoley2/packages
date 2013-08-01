#!/usr/bin/python3 -OO

import json
from random import choice
from config import APPKEY
from urllib.request import urlopen, Request


def get_categories():
    url = 'http://open.api.ebay.com/shopping'
    url += '?callname=GetCategoryInfo'
    url += '&CategoryID=-1'
    url += '&IncludeSelector=ChildCategories'
    req = Request(url)
    req.add_header('X-EBAY-API-RESPONSE-ENCODING', 'JSON')
    req.add_header('X-EBAY-API-VERSION', '733')
    req.add_header('X-EBAY-API-APP-ID', APPKEY)
    data = json.loads(urlopen(req).read().decode())
    categories = [category['CategoryID'] for category in data['CategoryArray']['Category']]
    categories.remove('-1')
    return categories


def get_item(category):
    url = 'http://svcs.ebay.com/services/search/FindingService/v1'
    url += '?itemFilter(0).name=FreeShippingOnly&itemFilter(0).value=true'
    url += '&itemFilter(1).name=MaxPrice&itemFilter(1).value=1'
    url += '&itemFilter(1).paramName=Currency&itemFilter(1).paramValue=USD'
    url += '&itemFilter(2).name=ListingType'
    url += '&itemFilter(2).value(0)=StoreInventory&itemFilter(2).value(1)=FixedPrice&itemFilter(2).value(2)=AuctionWithBIN'
    url += '&categoryId=' + category
    req = Request(url)
    req.add_header('X-EBAY-SOA-RESPONSE-DATA-FORMAT', 'json')
    req.add_header('X-EBAY-SOA-OPERATION-NAME', 'findItemsAdvanced')
    req.add_header('X-EBAY-SOA-SECURITY-APPNAME', APPKEY)
    data = json.loads(urlopen(req).read().decode())
    #print(json.dumps(data, indent=True))
    item = data['findItemsAdvancedResponse'][0]['searchResult'][0]
    if int(item['@count']) == 0:
        return None
    else:
        item = choice(item['item'])
    return item['title'][0]+' -- http://www.ebay.com/itm/'+item['itemId'][0]


def main():
    categories = get_categories()
    item = None
    while not item:
        item = get_item(choice(categories))
    print(item)

if __name__ == '__main__':
    main()
