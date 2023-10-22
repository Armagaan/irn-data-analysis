from Utills import TrainFX  as tfx
import json
from requests.exceptions import Timeout
import requests

t = tfx()
# trainInfo = t.getTrainInfo('14553')
trainname = t.getTrainList()
train_info_list = []

max_attempts = 3  # Maximum number of retry attempts

faulty_train = []
for train in trainname:
    attempts = 0
    while attempts < max_attempts:
        try:
            response = t.getTrainInfo(train, timeout=3)  # Set an appropriate timeout value
            response.raise_for_status()  # Raise an HTTPError for bad responses
            train_info = json.loads(response.text)
            print("Train: ", train, " Info received")
            if 'errorMessage' not in train_info:
                train_info_list.append(train_info)
            else:
                faulty_train.append(train)
                print(f"Faulty train number {train}")
            break  # Break out of the retry loop if successful
        except Timeout as e:
            print(f"Timeout error for train {train}. Retrying... ({attempts + 1}/{max_attempts})")
            attempts += 1
        except requests.RequestException as e:
            print(f"Request failed for train {train} with error: {e}")
            break  # Break out of the loop for other request errors

    if attempts == max_attempts:
        print(f"Error: Max attempts reached for train {train}")

# store the train_info_list in a new file
with open('train_info.json', 'w') as f:
    json.dump(train_info_list, f)


