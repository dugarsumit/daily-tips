import requests
import json
from config import config
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import schedule
import time
from random import randrange


creds = ServiceAccountCredentials.from_json_keyfile_dict(
    config["GOOGLE_CLIENT_SECRET_JSON"], scopes=config["SCOPES"]
)
gspread_client = gspread.authorize(creds)
HEADING_COL = 1
TIP_COL = 2
CODE_COL = 3
LINK_COL = 4
VIEW_COL = 5


def generate_content_map(cleaned_sheet):
    headings = cleaned_sheet[0]
    tips = cleaned_sheet[1]
    code = cleaned_sheet[2]
    links = cleaned_sheet[3]
    views = cleaned_sheet[4]
    view_count_content_map = {}
    for i in range(1, len(tips)):
        row = [i, headings[i], tips[i], code[i], links[i], views[i]]
        vcc_list = view_count_content_map.get(views[i], [])
        vcc_list.append(row)
        view_count_content_map[views[i]] = vcc_list
    view_count_content_map = dict(sorted(view_count_content_map.items()))
    return view_count_content_map


def clean_data(sheet):
    headings = sheet.col_values(1)
    tips = sheet.col_values(2)
    code = sheet.col_values(3)
    links = sheet.col_values(4)
    views = sheet.col_values(5)
    total = len(tips)
    if len(headings) < total:
        headings.extend((total-len(headings))*[''])
    if len(code) < total:
        code.extend((total-len(code))*[''])
    if len(links) < total:
        links.extend((total-len(links))*[''])
    if len(views) < total:
        views.extend((total-len(views))*[0])
    return [headings, tips, code, links, views]


def update_view_count(sheet, count, pos):
    sheet.update_cell(pos[0], pos[1], str(count))


def prepare_content():
    sheet = gspread_client.open(config["GOOGLE_SHEET_NAME"]).sheet1
    cleaned_sheet = clean_data(sheet)
    vcc_map = generate_content_map(cleaned_sheet)
    for view_count, content_list in vcc_map.items():
        if content_list:
            index = randrange(len(content_list))
            content = content_list[index]
            heading = content[1]
            tip = content[2]
            code = content[3]
            link = content[4]
            count = int(content[5]) + 1
            pos = [content[0]+1, VIEW_COL]
            break

    content = ''
    if heading:
        content += '*' + heading + '*' + '\n\n'
    if tip:
        content += '_' + tip + '_' + '\n\n'
    if code:
        content += '```' + code + '```' + '\n\n'
    if link:
        content += link + '\n\n'
    content += '-----------xxx-----------' + '\n\n'
    update_view_count(sheet, count, pos)
    return content


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
    post_content()
    scheduler()
    while True:
        print(".")
        schedule.run_pending()
        time.sleep(1)
