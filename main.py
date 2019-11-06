import requests
import json
from config import config
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import schedule
import time


creds = ServiceAccountCredentials.from_json_keyfile_dict(
    config["GOOGLE_CLIENT_SECRET_JSON"], scopes=config["SCOPES"]
)
gspread_client = gspread.authorize(creds)


def prepare_content():
    sheet = gspread_client.open(config["GOOGLE_SHEET_NAME"]).sheet1
    tips = sheet.col_values(2)
    print(tips, flush=True)
    return tips[-1]


def post_content():
    content = prepare_content()
    config["PAYLOAD"]["text"] = content
    json_payload = json.dumps(config["PAYLOAD"])
    requests.post(url=config["SLACK_WEBHOOK"], data=json_payload)


def scheduler():
    schedule.every().day.at("09:00").do(post_content)
    schedule.every().day.at("18:00").do(post_content)
    schedule.every().day.at("22:42").do(post_content)
    schedule.every().day.at("22:52").do(post_content)


if __name__ == "__main__":
    scheduler()
    while True:
        print(".")
        schedule.run_pending()
        time.sleep(1)
