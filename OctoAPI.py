from AllLibraries import *

CHROME_DRIVER = '.chromedriver'
LOCAL_API = 'http://localhost:58888/api/profiles'
OCTO_API_TOKEN = 'aa0b847b82f74d3c8566b74d2693d31a'
def get_octo_profiles(api_token):
    link_t = 'https://app.octobrowser.net/api/v2/automation/profiles?page_len=100&page=0&fields=title,description,proxy,start_pages,tags,status,last_active,version,storage_options,created_at,updated_at'
    data = requests.get(
        f'{link_t}', headers={'X-Octo-Api-Token': api_token}).json()
    return data