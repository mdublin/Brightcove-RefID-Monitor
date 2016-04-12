import json
import requests
import oauth_load

get_creds = oauth_load.loadSecret()
token = oauth_load.getAuthToken(get_creds)


def deactivate_request(bc_video_id):
    '''Ping Brightcove CMS with update_video POST request for asset deactivation'''
    
    url = "https://api.brightcove.com/services/post"
    headers = {'Content-Type': 'application/json'}
    print(headers)
    payload = 'json={"method":"update_video", "params":{"video":{"id":"%s", "itemState":"INACTIVE"}, "token":"jCoXH5OAMY16uOUSg_fEGDAdlhg.."}}' % bc_video_id
    
    # using params instead of data because we are making this POST request by
    # contructing query string URL with key/value pairs in it.
    r = requests.post(url, params=payload, headers=headers)
    print(r.status_code)
    #res = json.loads(r.text)
    #print(res)
    print(r.text)


#BC_cms_response = deactivate_request()
