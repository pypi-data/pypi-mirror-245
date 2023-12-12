import requests
import os
import pandas as pd

apiurl = "http://localhost:5000"

def get_table(database, period, source, tablename, 
    tablesubfolder=None, startdate=None, enddate=None, 
    symbols=None, portfolios=None, page=None, per_page=None):    

    url = apiurl+"/api/table/{database}/{period}/{source}/{tablename}"

    headers = {
        "Authorization": "Bearer "+os.environ['APITOKEN'],
        "Accept-Encoding": "gzip",
    }

    params = {
        'tablesubfolder': tablesubfolder,
        'startdate': startdate,
        'enddate': enddate,  
        'symbols': symbols,
        'portfolios': portfolios,  
        'page': page,
        'per_page': per_page
    }

    urlformat = url.format(database=database, period=period, source=source, tablename=tablename)
    response = requests.get(urlformat, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    js = response.json()
    df = pd.DataFrame(js['data']).set_index(js['pkey'])    
    return df.sort_index()

database = "MarketData"
period = "D1"
source = "THETADATA"
tablename = "QUOTES"
tablesubfolder = "202311"
startdate = "2023-11-17"
enddate = "2023-11-17"
df = get_table(database, period, source, tablename, 
    tablesubfolder=tablesubfolder, 
    startdate=startdate,
    enddate=enddate
)

idx = ['ES_' == x[:3] for x in df.index.get_level_values('symbol')]
df[idx]

