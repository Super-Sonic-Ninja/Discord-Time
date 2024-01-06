import time
import requests
import json
import urllib3
import warnings
from datetime import datetime

warnings.filterwarnings("ignore", category=urllib3.exceptions.InsecureRequestWarning)

def get_unix_time():
    return int(time.time())

def get_local_time():
    return datetime.now().strftime("%A, %d %B %Y %H:%M")

def format_discord_timestamp(current_unix_time):
    return f"<t:{current_unix_time}:F>"

def send_patch_request(authorization_token, bio):
    url = "https://discord.com/api/v9/users/@me/profile"
    headers = {
        "Authorization": authorization_token,
        "Content-Type": "application/json"
    }
    payload = {"bio": bio}

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=urllib3.exceptions.InsecureRequestWarning)
            response = requests.patch(url, headers=headers, data=json.dumps(payload), verify=False)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        pass

def load_config():
    try:
        with open("config.json", "r") as config_file:
            config_data = json.load(config_file)
            authorization_token = config_data.get("authorization_token", "")
            bio_template = config_data.get("bio", "")
            return authorization_token, bio_template
    except FileNotFoundError:
        return "", ""

def main():
    authorization_token, bio_template = load_config()

    if authorization_token:
        while True:
            current_unix_time = get_unix_time()
            discord_timestamp = format_discord_timestamp(current_unix_time)
            
            local_time = get_local_time()
            bio = bio_template.replace("{your_time}", local_time).replace("{current_time}", discord_timestamp)
            
            send_patch_request(authorization_token, bio)
            time.sleep(10)
    else:
        pass

if __name__ == "__main__":
    main()