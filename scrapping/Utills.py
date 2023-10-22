import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

class TrainFX():
    def getTrainList(self):
        response = requests.get('http://www.indianrail.gov.in/enquiry/FetchTrainData?_=1557752279434')
        datastore = json.loads(response.text)
        train_numbers = []
        for tr in datastore:
            train_numbers.append(tr.split('-')[0].strip())
        
        print("Found {} trains".format(len(train_numbers)))
        return train_numbers
    
    def getTrainInfo(self, train_number, timeout):
        unix_time = int(datetime.utcnow().timestamp()-1532)
        cookies = {
            '__gads' : 'ID=0b5cc381a6cc5d5e:T=1697635642:RT=1697635642:S=ALNI_MbSIbTJTVGP3rMCM8Xt4aDIub5Evg',
            '_gid' : 'GA1.3.1679543960.1697635644; _ga_SHTZYKNHG2=GS1.1.1697635639.1.1.1697635683.0.0.0',
            'JSESSIONID' : 'GA9C-MwGVJERPBL6MlhhbR39HY-Hq--Fog7TVrg5Lltr7FNiAraG!45373394; _ga=GA1.1.1336431025.1697635639',
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.irctc.co.in/nget/booking/check-train-schedule',
            'Content-Type': 'application/x-www-form-urlencoded',
            'greq': str(unix_time),
            'Content-Language': 'en',
            'Connection': 'keep-alive',
        }
        
        response = requests.get('https://www.irctc.co.in/eticketing/protected/mapps1/trnscheduleenquiry/'+train_number, headers=headers, timeout= timeout)
        return response



    