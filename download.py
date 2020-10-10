import requests
import csv
import time

API_KEY = 'QASZNQL3PG5W135Z'
stockList = "stockList.csv"

def initList():
    USList = []
    with open(stockList, newline='') as file:
        reader = [i for i in csv.DictReader(file)]
        for i in reader:
            if i['EXCHANGE'] == "New York Stock" or i['EXCHANGE'] == "Nasdaq":
                USList.append(i["TICKER"])
        print(USList)

def getOverveiw(symbol):
    result = requests.get("https://www.alphavantage.co/query?function=OVERVIEW&symbol="+symbol+"&apikey=QASZNQL3PG5W135Z")
    return result.json()

def getBalanceSheet(symbol):
    result = requests.get("https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol="+symbol+"&apikey=QASZNQL3PG5W135Z")
    return result.json()

def getCashFlow(symbol):
    result = requests.get("https://www.alphavantage.co/query?function=CASH_FLOW&symbol="+symbol+"&apikey="+API_KEY)
    return result.json()

def getPrice(symbol):
    result = requests.get("https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol="+symbol+"&apikey=" + API_KEY)
    return result.json()

def getDERatio(stock):
    totalLiabilities = float(stock.balancesheet["quarterlyReports"][0]["totalLiabilities"])
    totalEquity = float(stock.balancesheet["quarterlyReports"][0]["totalShareholderEquity"])
    DERatio = totalLiabilities/totalEquity
    return DERatio

def getPIRatio(stock):
    annualReports = [i for i in stock.cashflow["cashflow"]["annualReports"]]
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
    growth = float(stock.overview["PERatio"]) / float(stock.overview["PEGRatio"])
    totalEquity = float(stock.balancesheet["quarterlyReports"][0]["totalShareholderEquity"])
    value = (8.3459 * 1.07 ** growth) * averageFCF + totalEquity**0.8
    price = float(stock.price["Global Quote"]["05. price"])
    PIRatio = value / price
    return PIRatio


class stock():
    def __init__(self,symbol):
        self.overview = getOverveiw(symbol)
        self.cashflow = getCashFlow(symbol)
        self.balancesheet = getBalanceSheet(symbol)
        self.price = getPrice(symbol)
        self.PBRatio = float(self.overview["PriceToBookRatio"])
        self.profitMargin = float(self.overview["ProfitMargin"])
        self.PEGRatio = float(self.overview["PEGRatio"])
        self.dividendyield = float(self.overview["DividendYield"])
        self.returnOnEquity = float(self.overview["ReturnOnEquityTTM"])
        self.DERatio = getDERatio(self)
        self.PIRatio = getPIRatio(self)
    def getInfo(self):
        print("price: " + self.price + "\n")
        print("PBRatio: " + self.PBRatio + "\n")
        print("profitMargin: " + self.profitMargin + "\n")
        print("PEGRatio: " + self.PEGRatio + "\n")
        print("dividendyield: " + self.dividendyield + "\n")
        print("returnOnEquity: " + self.returnOnEquity + "\n")
        print("DERatio: " + self.DERatio + "\n")
        print("PIRatio: " + self.PIRatio + "\n")
    def getIndex(self):
        index = 7 * 


apple = stock("aapl")

apple.getInfo()