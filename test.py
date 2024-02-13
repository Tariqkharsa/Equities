import requests
import json
import csv

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key

'''
S.  Mehtab,  J.  Sen,  and  A.  Dutta,  “Stock  Price  Prediction  Using Machine  Learning  and  LSTM-Based  Deep  Learning  Models,” in Communications in Computer and Information Science, 2021, vol. 1366, pp. 88–106. doi: 10.1007/978-981-16-0419-5_8.

'''
url = 'https://www.alphavantage.co/query?function=CASH_FLOW&symbol=AAPL&apikey=Z6PXPFSGDHDLPPNR'
r = requests.get(url)
data = r.json()
data = data['annualReports']

# Define CSV file name
csv_file = 'financial_data.csv'

# Extract keys for the CSV header
keys = data[0].keys() if data else []

# Open CSV file in write mode
with open(csv_file, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=keys)

    # Write header
    writer.writeheader()

    # Write data
    for json_data in data:
        writer.writerow(json_data)