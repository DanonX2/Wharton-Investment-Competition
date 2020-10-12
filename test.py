import csv
def initList():
    USList = []
    with open("stockList.csv", newline='') as file:
        reader = [i for i in csv.DictReader(file)]
        for i in reader:
            if i['EXCHANGE'] == "New York Stock" or i['EXCHANGE'] == "Nasdaq":
                USList.append(i["TICKER"])
        return USList

print(initList())