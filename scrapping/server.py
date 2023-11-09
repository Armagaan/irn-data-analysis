# from Utills import TrainFX
import json
from requests.exceptions import Timeout
import requests
import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import date, datetime,timedelta
import pickle
train_info_list = []

max_attempts = 4  # Maximum number of retry attempts

faulty_train = []

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
    
    def getTrainDelay(self, train_number = '', timeout=10):
        unix_time = int(datetime.utcnow().timestamp()-1532)
        cookies = {
            '__gads' : 'ID=0b5cc381a6cc5d5e:T=1697635642:RT=1697635642:S=ALNI_MbSIbTJTVGP3rMCM8Xt4aDIub5Evg',
            '_gid' : 'GA1.3.1679543960.1697635644; _ga_SHTZYKNHG2=GS1.1.1697635639.1.1.1697635683.0.0.0',
            'JSESSIONID' : 'GA9C-MwGVJERPBL6MlhhbR39HY-Hq--Fog7TVrg5Lltr7FNiAraG!45373394; _ga=GA1.1.1336431025.1697635639',
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            # 'Referer': 'https://www.irctc.co.in/nget/booking/check-train-schedule',
            'Content-Type': 'text/html; charset=UTF-8',
            'greq': str(unix_time),
            # 'Content-Language': 'en',
            'Connection': 'keep-alive',
        }
        url = f"https://etrain.info/train/{train_number}/history?d=3"
        response = requests.get(url, headers=headers, timeout= timeout)
        soup = BeautifulSoup(response.content, 'html.parser')
        pattern = re.compile(r'\((.*?)\)')
        section_links = soup.find_all('a', class_='runStatStn')
        section_data = []
        station_delay = {}
        for link in section_links:
            section_name = link.find('div').text.strip()
            avg_delay_text = link.find('div', class_='inlineblock pdl5').text
            avg_delay = int(avg_delay_text.split(':')[1].strip().split(' ')[0])
            section_data.append({'section_name': section_name, 'avg_delay': avg_delay})
            clean_section_name = section_name.replace("\r\n\t\t\t\t\t\t\t\t\nAvg. Delay: ", '')
            station_delay[clean_section_name] = avg_delay

        # for data in section_data:
        #     print(f"Section: {data['section_name']}, Avg. Delay: {data['avg_delay']} Min's")
        station_delay = {pattern.search(key).group(1): value for key, value in station_delay.items()}
        return response, station_delay
    

def getTrainDelayOnDate(train_no, date, timeout = 5):
    unix_time = int(datetime.utcnow().timestamp()-1532)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        # 'Referer': 'https://www.irctc.co.in/nget/booking/check-train-schedule',
        'Content-Type': 'text/html; charset=UTF-8',
        'greq': str(unix_time),
        # 'Content-Language': 'en',
        'Connection': 'keep-alive',
    }
    base_url = "https://runningstatus.in/check.php"
    params = {
        'a': 'history',
        'trainno': train_no,
        'duration': 'seldates',
        'fdate': date,
        'tdate': date
    }
    response = requests.get(base_url, params=params, timeout = timeout)
    soup = BeautifulSoup(response.content, 'html.parser')
    delay_table = soup.find('table', class_='table-striped')
    if delay_table is None :
        return response, {}
    date_station_delay = {}
    tds = delay_table.find_all('td', {'class': None, 'style': None})
    stations = tds[::2]  # Select every second td element
    delays = delay_table.find_all('span', class_='text-danger')
    delays = [td.find('span', class_='text-danger') for td in tds[1::2]]

    for station, delay in zip(stations, delays):
        station_name = station.find('abbr').get('title')
        distance = station.find('small').text
        delay_time = delay.text.strip() if delay else ''
        date_station_delay[station_name] = delay_time
    
    return response, date_station_delay

def getDelayForAllDates(train_no):
    # https://runningstatus.in/check.php?a=history&trainno=12145&duration=seldates&fdate=03-11-2023&tdate=04-11-2023
    
    start_date = date(2022, 11, 1)
    end_date = date(2023, 10, 31)

    current_date = start_date
    train_delay_dict = {}
    while current_date <= end_date:
        formatted_date = current_date.strftime("%d-%m-%Y")
        attempts = 0
        while attempts < max_attempts:
            try:
                response, train_date_dict = getTrainDelayOnDate(train_no, formatted_date)  # Set an appropriate timeout value
                response.raise_for_status()  # Raise an HTTPError for bad responses
                # print("Train: ", train_no, " delay for ", formatted_date, " received")
                train_delay_dict[formatted_date] = train_date_dict
                break  # Break out of the retry loop if successful
            except Timeout as e:
                print(f"Timeout error for train {train_no}. Retrying... ({attempts + 1}/{max_attempts})")
                attempts += 1
            except requests.RequestException as e:
                train_with_no_delay_data.append(train_no)
                print(f"Request failed for train {train_no} with error: {e}")
                break  # Break out of the loop for other request errors
            if attempts == max_attempts:
                print(f"Error: Max attempts reached for train {train_no} on date {formatted_date}")
        
        current_date += timedelta(days=1)
    return train_delay_dict



with open('train_info.json', 'r') as file:
    data = json.load(file)
train_numbers = [entry.get("trainNumber") for entry in data]
print(train_numbers)
# train_numbers = ['14233', '20665', '22224', '22439', '20979']
import numpy as np

num_parts = 8
split_arrays = np.array_split(train_numbers, num_parts)
train_with_no_delay_data = []

import json
import threading

def process_part(part_index, train_with_no_delay_data):
    train_numbers = split_arrays[part_index]
    final_train_delay_data = {}
    for train in train_numbers:
        t = getDelayForAllDates(train)
        if not t:
            train_with_no_delay_data.append(train)
            continue
        final_train_delay_data[train] = t

    with open(f'./data/train_delay_22_23_{part_index + 1}.json', 'w') as f:
        json.dump(final_train_delay_data, f)

threads = []
for i in range(num_parts):
    thread = threading.Thread(target=process_part, args=(i, train_with_no_delay_data))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()


# for i in range(num_parts):
#     train_numbers = split_arrays[i]
#     final_train_delay_data = {}
#     for train in train_numbers:
#         t = getDelayForAllDates(train)
#         if t == {}:
#             train_with_no_delay_data.append(train)
#             continue
#         final_train_delay_data[train] = t
#     with open(f'train_delay_22_23_{i + 1}.json', 'w') as f:
#         json.dump(final_train_delay_data, f)

print(train_with_no_delay_data)
with open('train_with_no_delay.pkl', 'wb') as file:
    # Write each element of the list to a new line in the file
    pickle.dump(train_with_no_delay_data, file)