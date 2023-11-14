import json

file_r = "data/train_info.json"
file_w = "data/train_info_new.json"

with open(file_r) as file:
    info = json.load(file)

info_new = {}
for d in info:
    if "stationList" not in d.keys():
        continue
    train_num = d["trainNumber"]
    info_new[train_num] = d
    station_dict = {}
    for station in d["stationList"]:
        station_code = station["stationCode"]
        station_dict[station_code] = station
    info_new[train_num]["stationDict"] = station_dict
    del info_new[train_num]["stationList"]

with open(file_w, "w") as file:
    json.dump(info_new, file)
