# -*- coding: utf-8 -*-
#%%
#
# Trigger-based home electrical appliance controller using nature remo
#

#import modules
import datetime as dt
import json
import yaml
import csv
import requests
import sys

#Flag
DEBUG = False
DRY_RUN = False

#file path
conf_file = "conf/config.yaml"
id_file = "conf/id.yaml"
holiday_file = "conf/holiday.json"
log_file = "logs/ctrl_main.txt"

temp_file = "../logging/logs/temp.txt"
hu_file = "../logging/logs/hu.txt"
il_file = "../logging/logs/il.txt"
mo_file = "../logging/logs/mo.txt"
aircon_file = "../logging/logs/aircon_state.txt"


#global setting
execute_interval = 4 #min

def load_yaml(file_path):
    with open(file_path) as file:
        return yaml.safe_load(file)

def load_json(file_path):
    with open(file_path, encoding="utf-8_sig") as file:
        return json.load(file)

def load_csv(file_path):
    with open(file_path) as file:
        reader = csv.reader(file, skipinitialspace=True)
        l = [row for row in reader]
        return l

def national_holiday() :
    today_str = dt.datetime.now().strftime("%Y-%m-%d")
    holiday_list = load_json(holiday_file)

    return (today_str in holiday_list)

def holiday() :
    weekday = dt.date.today().weekday()
    return (weekday >= 5) or national_holiday()

def get_last_temp() :
    temp_data = load_csv(temp_file)
    return float(temp_data[len(temp_data)-1][1])

def get_last_hu() :
    hu_data = load_csv(hu_file)
    return float(hu_data[len(hu_data)-1][1])

def get_last_il() :
    li_data = load_csv(il_file)
    return float(li_data[len(li_data)-1][1])

def get_last_mo() :
    mo_data = load_csv(mo_file)
    return dt.datetime.strptime(mo_data[len(mo_data)-1][0], '%Y-%m-%dT%H:%M:%SZ')+dt.timedelta(hours=9)

def get_last_aircon_state() :
    aircon_data = load_csv(aircon_file)
    last_aircon_power = aircon_data[len(aircon_data)-1][1]
    last_aircon_mode = aircon_data[len(aircon_data)-1][2]
    last_aircon_temp = aircon_data[len(aircon_data)-1][3]
    return last_aircon_power, last_aircon_mode, last_aircon_temp

def eval_trigger(trigger) :
    dt_now = dt.datetime.now()
    dt_now_date_str = dt_now.strftime("%Y-%m-%d")

    matched = {}
    for keyword in trigger :
        if keyword == "DOW" :
            if (trigger["DOW"] == "weekday") and not holiday() :
                matched["DOW"] = True
            elif (trigger["DOW"] == "holiday") and holiday() :
                matched["DOW"] = True
            else:
                matched["DOW"] = False
        elif keyword == "TIME" :
            dt_target = dt.datetime.strptime(dt_now_date_str+"T"+trigger["TIME"], '%Y-%m-%dT%H:%M')
            td = dt.timedelta(minutes=execute_interval)
            if abs(dt_target-dt_now) < td :
                matched["TIME"] = True
            else:
                matched["TIME"] = False
        elif keyword == "START-TIME" :
            dt_target = dt.datetime.strptime(dt_now_date_str+"T"+trigger["START-TIME"], '%Y-%m-%dT%H:%M')
            if dt_target <= dt_now :
                matched["START-TIME"] = True
            else:
                matched["START-TIME"] = False
        elif keyword == "END-TIME" :
            dt_target = dt.datetime.strptime(dt_now_date_str+"T"+trigger["END-TIME"], '%Y-%m-%dT%H:%M')
            if dt_target >= dt_now :
                matched["END-TIME"] = True
            else:
                matched["END-TIME"] = False
        elif keyword == "TEMP" :
            target_temp = trigger["TEMP"].split("C")
            last_temp = get_last_temp()
            if (target_temp[1] == "+") and (float(target_temp[0]) <= last_temp) :
                matched["TEMP"] = True
            elif (target_temp[1] == "-") and (float(target_temp[0]) >= last_temp) :
                matched["TEMP"] = True
            else:
                matched["TEMP"] = False
        elif keyword == "HU" :
            target_hu = trigger["HU"].split("H")
            last_hu = get_last_hu()
            if (target_hu[1] == "+") and (float(target_hu[0]) <= last_hu) :
                matched["HU"] = True
            elif (target_hu[1] == "-") and (float(target_hu[0]) >= last_hu) :
                matched["HU"] = True
            else:
                matched["HU"] = False
        elif keyword == "IL" :
            target_il = trigger["IL"].split("L")
            last_il = get_last_il()
            if (target_il[1] == "+") and (float(target_il[0]) <= last_il) :
                matched["IL"] = True
            elif (target_il[1] == "-") and (float(target_il[0]) >= last_il) :
                matched["IL"] = True
            else:
                matched["IL"] = False
        elif keyword == "MOTION" :
            target_mo = trigger["MOTION"].split("_")
            target_past_time = target_mo[1][:-1]
            target_past_time_unit = target_mo[1][-1]
            if target_past_time_unit != "m" :
                print("[Trigger(motion)] Unrecognized unit: ", target_past_time_unit)
            
            last_mo = get_last_mo()
            td = dt.timedelta(minutes=int(target_past_time))
            if (target_mo[0] == "NO"):
                if (abs(last_mo - dt_now) >= td) :
                    matched["MOTION"] = True
                else:
                    matched["MOTION"] = False
            elif (target_mo[0] == "YES"):
                if (abs(last_mo - dt_now) <= td) :
                    matched["MOTION"] = True
                else:
                    matched["MOTION"] = False

        else:
            print("Trigger ", keyword, " not defined.")
    return matched

def send_ir_signal(token, signal_id):
    headers = {"Authorization": 'Bearer '+token}
    result = requests.post("https://api.nature.global/1/signals/"+signal_id+"/send", headers=headers)
    
    return result

def send_aircon_signal(token, aircon_id, power, mode=None, temp=None):
    url = "https://api.nature.global/1/appliances/"+aircon_id+"/aircon_settings"
    headers = {"Authorization": 'Bearer '+token}
    data_send = {}

    if (mode == "cool") or (mode == "c") :
        data_send["operation_mode"] = "cool"
    elif (mode == "warm") or (mode == "w") :
        data_send["operation_mode"] = "warm"
    elif (mode == "dry") or (mode == "d") :
        data_send["operation_mode"] = "dry"
    
    if temp != None :
        data_send["temperature"] = str(temp)

    if power == "off" :
        data_send["button"] = "power-off"
    else :
        data_send["button"] = ""

    result = requests.post(url, headers=headers, data=data_send)
    
    return result

def push_message(token, title, body):
	url = "https://api.pushbullet.com/v2/pushes"
	
	headers = {"content-type": "application/json", "Authorization": 'Bearer '+token}
	data_send = {"type": "note", "title": title, "body": body}

	_r = requests.post(url, headers=headers, data=json.dumps(data_send))

def send_pushmessage(token, res, body):
    if res.status_code == 200 :
        push_message(token, "Remo", body)
    else:
        push_message(token, "Remo (ERROR)", "code:"+res.status_code)

def main():
    start_time = dt.datetime.now()

    id_list = load_yaml(id_file) #signal and appliance id list
    config_list = load_yaml(conf_file) #trigger-config file
    token = id_list["token"]
    executed_list = {}

    for cmd in config_list:
        cmd_name = list(cmd.keys())[0]

        if ("Trigger" in cmd[cmd_name]) and ("Execute" in cmd[cmd_name]) :
            #matching trigger
            trigger = cmd[cmd_name]["Trigger"]
            matched = eval_trigger(trigger)
            if DEBUG : print("Check trigger (",cmd_name,"):",matched)

            #execute command
            if all(matched.values()) == True :
                if ("TARGET" not in cmd[cmd_name]["Execute"]) or ("MODE" not in cmd[cmd_name]["Execute"]) :
                    print("TARGET or MODE not found in ", cmd_name)
                    sys.exit()

                target_app =  cmd[cmd_name]["Execute"]["TARGET"]
                target_mode = cmd[cmd_name]["Execute"]["MODE"]

                if target_app not in executed_list :
                    print("@@ Trigger", cmd_name,"activated. @@")

                    if target_app == "Air-con" :
                        current_aircon_power, current_aircon_mode, current_aircon_temp = get_last_aircon_state()
                        target_aircon_setting = target_mode.split("-")
                        target_aircon_mode = target_aircon_setting[0]
                        if len(target_aircon_setting) == 2 :
                            target_aircon_temp = target_aircon_setting[1][:-1]
                        else:
                            target_aircon_temp = "NaN"
                        
                        if (target_mode == "off") :
                            if (current_aircon_power != target_mode) :
                                print("** SEND SIGNAL (", cmd_name, ") Command=", cmd[cmd_name]["Execute"], "**")
                                executed_list[target_app] = True
                                if not DRY_RUN :
                                    res = send_aircon_signal(token, id_list[target_app]["id"], "off")
                                    if "push_token" in id_list : send_pushmessage(id_list["push_token"], res, "Air-con : Power off\ncmd:"+cmd_name)

                        elif (target_aircon_mode == "cool") or (target_aircon_mode == "warm") or (target_aircon_mode == "dry") :
                            if (current_aircon_mode != target_aircon_mode) or (current_aircon_temp != target_aircon_temp) :
                                print("** SEND SIGNAL (", cmd_name, ") Command=", cmd[cmd_name]["Execute"], "**")
                                executed_list[target_app] = True
                                if not DRY_RUN :
                                    res = send_aircon_signal(token, id_list[target_app]["id"], "on", target_aircon_mode, target_aircon_temp)
                                    if "push_token" in id_list : send_pushmessage(id_list["push_token"], res, "Air-con : "+str(target_mode)+"\ncmd:"+cmd_name)
                        
                    else:
                        print("** SEND SIGNAL (", cmd_name, ") Command=", cmd[cmd_name]["Execute"], "**")
                        executed_list[target_app] = True
                        if not DRY_RUN :
                            res = send_ir_signal(token, id_list[target_app][target_mode])
                            if "push_token" in id_list : send_pushmessage(id_list["push_token"], res, "target:"+target_app+"\nmode:"+target_mode+"\ncmd:"+cmd_name)

        else:
            print("Trigger or Execute not found in ", cmd_name)
            sys.exit()
    
    print("TIME:", start_time.strftime("%Y-%m-%d %H:%M:%S"),  "TEMP:", get_last_temp(), " HU:", get_last_hu(), " IL:", get_last_il(), " MO:", get_last_mo())

#%%
main()

# %%
