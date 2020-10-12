import requests
import csv
import time

API_KEY = 'S2AEUWYBR1CP7OX7'
stockList = "stockList.csv"

def initList():
    USList = []
    with open(stockList, newline='') as file:
        reader = [i for i in csv.DictReader(file)]
        for i in reader:
            if i['EXCHANGE'] == "New York Stock" or i['EXCHANGE'] == "Nasdaq":
                USList.append(i["TICKER"])
        return USList

def getOverveiw(symbol):
    result = "https://www.alphavantage.co/query?function=OVERVIEW&symbol="+symbol+"&apikey=S2AEUWYBR1CP7OX7"
    result = requests.get(result).json()
    return result

def getBalanceSheet(symbol):
    result = requests.get("https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol="+symbol+"&apikey=S2AEUWYBR1CP7OX7")
    return result.json()

def getCashFlow(symbol):
    result = requests.get("https://www.alphavantage.co/query?function=CASH_FLOW&symbol="+symbol+"&apikey="+API_KEY)
    return result.json()

def getDERatio(stock):
    totalLiabilities = float(stock.balancesheet["quarterlyReports"][0]["totalLiabilities"])
    totalEquity = float(stock.balancesheet["quarterlyReports"][0]["totalShareholderEquity"])
    DERatio = totalLiabilities/totalEquity
    return DERatio

def getPIRatio(stock):
    annualReports = [i for i in stock.cashflow["annualReports"]]
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
    growth = float(stock.overview["PERatio"]) / (float(stock.overview["PEGRatio"]) + 1)
    totalEquity = float(stock.balancesheet["quarterlyReports"][0]["totalShareholderEquity"])
    value = (8.3459 * 1.07 ** growth) * averageFCF + totalEquity**0.8
    shares = float(stock.overview["SharesOutstanding"])
    PIRatio = value / shares
    return PIRatio


class stock():
    def __init__(self,symbol):
        self.status = False
        self.overview = getOverveiw(symbol)
        self.cashflow = getCashFlow(symbol)
        self.balancesheet = getBalanceSheet(symbol)
        self.profitMargin = float(self.overview["ProfitMargin"])
        self.PBRatio = float(self.overview["PriceToBookRatio"])
        try:self.PEGRatio = float(self.overview["PEGRatio"])
        except:self.PEGRatio = 1
        self.dividendyield = float(self.overview["DividendYield"])
        self.returnOnEquity = float(self.overview["ReturnOnEquityTTM"])
        try:self.DERatio = getDERatio(self)
        except:self.DERatio = 0.2
        try:self.PIRatio = getPIRatio(self)
        except:self.PIRatio = 1
        self.index = self.getIndex()
    def getInfo(self):
        print("PBRatio: " + self.PBRatio + "\n")
        print("profitMargin: " + self.profitMargin + "\n")
        print("PEGRatio: " + self.PEGRatio + "\n")
        print("dividendyield: " + self.dividendyield + "\n")
        print("returnOnEquity: " + self.returnOnEquity + "\n")
        print("DERatio: " + self.DERatio + "\n")
        print("PIRatio: " + self.PIRatio + "\n")
        print("index: " + self.index + "\n")
    def getIndex(self):
        self.index = 1.015 ** self.PIRatio + 0.2 * self.DERatio + 0.2 *(1.01 ** self.PBRatio) + 0.3 * self.dividendyield + 0.5 * self.returnOnEquity + 0.4 * self.profitMargin + 0.6 * (1.01 ** self.PEGRatio)
        self.index /= 2.2
        return self.index

USList = initList()
Stocks = []
counter = 0
with open('results.csv', 'w', newline='',buffering=1) as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Ticker', 'PBRatio','profitMargin','PEGRatio','dividendyield','returnonequity','DERatio','PIRatio','index'])
        csvfile.flush()
        print('output file set-up success')
for i in USList[-33:]:
    with open('results.csv', 'a', newline='',buffering=1) as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        success = False
        while success == False:
            try:
                Stocks.append(stock(i))
                success = True
            except:
                time.sleep(1)
                print("reached API Limit, retrying...")
        writer.writerow([i,Stocks[counter].PBRatio,Stocks[counter].profitMargin,Stocks[counter].PEGRatio,Stocks[counter].dividendyield,Stocks[counter].returnOnEquity,Stocks[counter].DERatio,Stocks[counter].PIRatio,Stocks[counter].index])
        csvfile.flush()
        counter += 1
        print(i,"Done\n")