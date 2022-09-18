import sys
import json
import requests

def get_fork_info():

    ODSCORP_API = 'http://api.oddscp.com:8111/forks?bk2_name=gg_bet,pinnacle&min_fi=0,1&token=0d483739b670f1a2b38feeca99f5eddc'
    r = requests.get(ODSCORP_API)
    forks = json.loads(r.text)

    list_fork_info = []
    for fork in forks:
        #print(fork)
        list_fork_info.append([fork['sport'] + " | " + fork['BK1_game'] + " | " + fork['bet_type'], fork['alive_sec']])


    #print(list_fork_info)
    return list_fork_info

