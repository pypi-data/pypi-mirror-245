import requests
import json


def send_teams_webhook(
    webhook_url,
    main_title="",
    main_msg="",
    activity_title="",
    activity_msg="",
    theme_color="#0000FF",
):
    theme_color = theme_color
    # teams_webhook_url = "https://shinsegaegroup.webhook.office.com/webhookb2/f6ed8cf6-f350-482a-aa1d-ed7fd262d466@d4ffc887-d88d-41cc-bf6a-6bb47ec0f3ca/IncomingWebhook/2868210da0d24639b1413c093bf3da9a/ca7346bc-3396-46fe-9cba-7a9c18460e7d"

    headers = {"Content-Type": "application/json"}

    message_to_send = {
        "title": main_title,
        "text": main_msg,
        "themeColor": theme_color,
        "sections": [{"activityTitle": activity_title, "text": activity_msg}],
    }
    response = requests.post(webhook_url, json=message_to_send, headers=headers)

    if not response.status_code == 200:
        print(f"Send Webhook Failed!: {response.status_code}, {response.text}")
