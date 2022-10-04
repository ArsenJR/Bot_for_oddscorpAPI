from AllLibraries import *


def get_fork_info():
    ODSCORP_API = 'http://api.oddscp.com:8111/forks?bk2_name=gg_bet,pinnacle&min_fi=0,1&token=0d483739b670f1a2b38feeca99f5eddc'
    r = requests.get(ODSCORP_API)
    forks = json.loads(r.text)
    forks = sorted(forks, key=itemgetter('alive_sec'), reverse=True)
    list_fork_info = []
    list_fork_alive = []
    for fork in forks:
        list_fork_info.append(fork['sport'] + " | " + fork['BK1_game'] + " | " + fork['bet_type'])
        list_fork_alive.append(fork['alive_sec'])

    return [list_fork_info, list_fork_alive, forks]

def get_fork_to_bet():
    ODSCORP_API = 'http://api.oddscp.com:8111/forks?bk2_name=gg_bet,pinnacle&min_fi=0,1&token=0d483739b670f1a2b38feeca99f5eddc'
    r = requests.get(ODSCORP_API)
    forks = json.loads(r.text)
    list_fork_info = []
    list_fork_id = []
    for fork in forks:
        list_fork_info.append(fork['sport'] + " | " + fork['BK1_game'] + " | " + fork['bet_type'])
        list_fork_id.append(fork['fork_id'])
    return list_fork_info, list_fork_id, forks