from datetime import datetime, timedelta
import requests
import json
import os


TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.00Z"

end_time = datetime.now().strftime(TIMESTAMP_FORMAT)
start_time = (datetime.now() + timedelta(days=-1)).strftime(TIMESTAMP_FORMAT)

query = "bolhadev"

tweet_fields = "tweet.fields=author_id,conversation_id,created_at,id,in_reply_to_user_id,public_metrics,lang,text"
user_fields = "expansions=author_id&user.fields=id,name,username,created_at"

url_raw = f"https://api.twitter.com/2/tweets/search/recent?query={query}&{tweet_fields}&{user_fields}&start_time={start_time}&end_time={end_time}"

print(url_raw)

bearer_token = os.environ.get("TBEARERTOKEN")
headers = {"Authorization": "Bearer {}".format(bearer_token)}
response = requests.request("GET", url_raw, headers=headers)

json_reponse = response.json()
print(json.dumps(json_reponse, indent=4, sort_keys=True, ensure_ascii=True))

while "next_token" in json_reponse.get("meta", {}):
    next_token = json_reponse['meta']['next_token']
    url = f"{url_raw}&next_token={next_token}"
    response = requests.request("GET", url=url, headers=headers)
    json_reponse = response.json()
    print(json.dumps(json_reponse, indent=4, sort_keys=True, ensure_ascii=True))