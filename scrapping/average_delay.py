# from Utills import TrainFX
import json
from requests.exceptions import Timeout
import requests
import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import date, datetime,timedelta
train_info_list = []

max_attempts = 3  # Maximum number of retry attempts


def getTrainDelay(train_number = '', timeout=10):
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


train_info = ''
train_with_no_delay_data = []
train_delay_dict = {}


with open('train_info.json', 'r') as file:
    data = json.load(file)
train_numbers = [entry.get("trainNumber") for entry in data]

print(train_numbers)
for train in train_numbers:
    attempts = 0
    while attempts < max_attempts:
        try:
            response, train_delay = getTrainDelay(train, timeout=3)  # Set an appropriate timeout value
            response.raise_for_status()  # Raise an HTTPError for bad responses
            if 'errorMessage' not in train_info:
                print("Train: ", train, " Info received")
                train_delay_dict[train] = train_delay
            else:
                print(f"Faulty train number {train}")
            break  # Break out of the retry loop if successful
        except Timeout as e:
            print(f"Timeout error for train {train}. Retrying... ({attempts + 1}/{max_attempts})")
            attempts += 1
        except requests.RequestException as e:
            train_with_no_delay_data.append(train)
            print(f"Request failed for train {train} with error: {e}")
            break  # Break out of the loop for other request errors

    if attempts == max_attempts:
        print(f"Error: Max attempts reached for train {train}")

# store the train_info_list in a new file
with open('train_average_delay.json', 'w') as f:
    json.dump(train_delay_dict, f)
