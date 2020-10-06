import requests

API_KEY = 'QASZNQL3PG5W135Z'

def getOverveiw(symbol):
    result = requests.get("https://www.alphavantage.co/query?function=OVERVIEW&symbol="+symbol+"&apikey=QASZNQL3PG5W135Z")
    return result.json()

def getBalanceSheet(symbol):
    result = requests.get("https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol="+symbol+"&apikey=QASZNQL3PG5W135Z")
    return result.json()

def getPBRatio(overview):
    return float(overview["PriceToBookRatio"])

def getProfitMargin(overview):
    return float(overview["ProfitMargin"])

def getPEGRatio(overview):
    return float(overview["PEGRatio"])

def getDividendYield(overview):
    return float(overview["DividendYield"])

def getReturnOnEquity(overview):
    return float(overview["ReturnOnEquityTTM"])

def getDERatio(bSheet):
    totalLiabilities = float(bSheet["quarterlyReports"][0]["totalLiabilities"])
    totalEquity = float(bSheet["quarterlyReports"][0]["totalShareholderEquity"])
    DERatio = totalLiabilities/totalEquity
    return DERatio


apple = getOverveiw("aapl")
appleb = getBalanceSheet("aapl")
print(getDERatio(appleb))