import json
from urllib.parse import unquote_plus
import requests
from datetime import datetime


webhook_msg = []
main_msg = []


def run_nes_api(notebook_params):
    global webhook_msg

    nes_url = "https://nes.shinsegae.ai/v1/runs"

    nes_headers = {
        "Content-Type": "application/json",
        "accept": "application/json",
    }

    nes_params = {
        "input_url": "https://github.com/emartdt/datafabric-notebooks/blob/main/etl/autoload/s3_to_bq_autoload.ipynb",
        "parameters": notebook_params,
        "runtime": "",
        "host_network": True,
    }
    json_params = json.dumps(nes_params)

    response = requests.post(nes_url, headers=nes_headers, data=json_params)

    if response.status_code == 200 | 201:
        response_data = response.json()
        webhook_msg.append(f"[Commuter]({response_data.get('output_url')})")
        return True
    else:
        webhook_msg.append(
            f"NES Request failed with status code : {response.status_code}"
        )
        response_data = response.content
        webhook_msg.append(f"Response MSG : {response_data}")
        return False


def send_teams_webhook(webhook_url):
    global main_msg, webhook_msg

    default = "https://shinsegaegroup.webhook.office.com/webhookb2/f6ed8cf6-f350-482a-aa1d-ed7fd262d466@d4ffc887-d88d-41cc-bf6a-6bb47ec0f3ca/IncomingWebhook/2868210da0d24639b1413c093bf3da9a/ca7346bc-3396-46fe-9cba-7a9c18460e7d"

    teams_webhook_url = webhook_url if webhook_url else default

    current = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    main_msg.append(f"* AWS Lambda Runtime : {current}")

    headers = {"Content-Type": "application/json"}

    message_to_send = {
        "title": "[AWS to BigQuery Autoload Report]",
        "text": "\n".join(main_msg),
        "themeColor": "#0000FF",
        "sections": [{"activityTitle": "NES 실행 결과", "text": "\n".join(webhook_msg)}],
    }
    response = requests.post(teams_webhook_url, json=message_to_send, headers=headers)

    if not response.status_code == 200:
        print(f"Send Webhook Failed!: {response.status_code}, {response.text}")


def isAllowedExtension(extension):
    global webhook_msg

    # parquet의 경우 해당 폴더에 _SUCCESS 파일 생성 시 '*.parquet'으로 Read
    allowed_extensions = ["csv", "json", "_success"]
    if extension.lower() in allowed_extensions:
        return True
    else:
        if extension.lower() == "schema":
            webhook_msg.append(f"Schema File Uploaded.")
        else:
            webhook_msg.append(f"Validate file format. Input format : {extension}\n")
        return False
    # raise Exception("This extension is not supported : {}, Only support csv/json/parquet".format(extension))


def s3_autoload(event, webhook_url=""):
    global webhook_msg, main_msg

    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = unquote_plus(event["Records"][0]["s3"]["object"]["key"], encoding="utf-8")

    print(f">>> Call Lambda Handler : {key}")
    paths = key.split("/")
    project = "emart-datafabric"
    dataset = "temp_7d"
    table = ".".join(paths[-1].split(".")[0:-1])

    file = paths[-1]
    extension = file.split(".")[-1]

    if len(paths) > 2:
        project = paths[0]
        dataset = paths[1]
        table = paths[2]

    user_ip = event["Records"][0]["requestParameters"]["sourceIPAddress"]
    size = event["Records"][0]["s3"]["object"]["size"]
    timeCreated = event["Records"][0]["eventTime"]
    eventName = event["Records"][0]["eventName"]

    # TODDO: Make: eventName 기준으로 update면 updated 사용
    data = {
        "bucket": bucket,
        "key": key,
        "project": project,
        "dataset": dataset,
        "table": table,
        "file": file,
        "extension": extension,
        "user_ip": user_ip,
        "size": f"{size}",
        "timeCreated": timeCreated,
        "updated": timeCreated,
        "eventName": eventName,
    }

    for key, value in data.items():
        main_msg.append(f"* {key} : {value}\n")

    try:
        print(json.dumps(data, indent=2))

        if isAllowedExtension(extension):
            run_nes_api(data)
            send_teams_webhook(webhook_url)

        # Cloudfunction에서 메시지 중첩되어 보냄. 그래서 초기화 코드 추가
        webhook_msg = []
        main_msg = []
        return True
    except Exception as e:
        print(e)
        raise e
