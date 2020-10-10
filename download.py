import requests

API_KEY = 'QASZNQL3PG5W135Z'

def getOverveiw(symbol):
    result = requests.get("https://www.alphavantage.co/query?function=OVERVIEW&symbol="+symbol+"&apikey=QASZNQL3PG5W135Z")
    return result.json()

def getBalanceSheet(symbol):
    result = requests.get("https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol="+symbol+"&apikey=QASZNQL3PG5W135Z")
    return result.json()

def getCashFlow(symbol):
    result = requests.get("https://www.alphavantage.co/query?function=CASH_FLOW&symbol="+symbol+"&apikey="+API_KEY)
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

def getPIRatio(symbol):
    annualReports = [i for i in symbol[cashFlow["cashflow"]["annualReports"]]
    FCF = [0 for i in range(len(annualReports))]
    counter = 0
    for i in annualReports:
        FCF[counter] = float(i["operatingCashflow"]) - float(i["capitalExpenditures"])
        counter += 1
    averageFCF = 0
    counter = 0
    for i in FCF:
        averageFCF+=i
        counter += 1
    averageFCF /= counter
    growth = float(symbol["overview"]["PERatio"]) / float(symbol["overview"]["PEGRatio"])
    totalEquity = float(symbol["balancesheet"]["quarterlyReports"][0]["totalShareholderEquity"])
    value = (8.3459 * 1.07 ** growth) * averageFCF + totalEquity**0.8
    price = symbol["daily"]["Time Series (Daily)"][]
    PIRatio = float(symbol["overview"][""])
    return averageFCF

apple = getOverveiw("aapl")
appleb = getBalanceSheet("aapl")
print(getPIRatio(getCashFlow("aapl")))