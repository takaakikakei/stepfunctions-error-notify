import json
import logging
import requests
import boto3
import os
import re

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Get credentials
secret_name = os.environ["SECRET_NAME"]
secretsmanager_client = boto3.client("secretsmanager", region_name="ap-northeast-1")
resp = secretsmanager_client.get_secret_value(SecretId=secret_name)
secret = json.loads(resp["SecretString"])

ALERT_HIGH_CHANNEL_WEBHOOK = secret["ALERT_HIGH_CHANNEL_WEBHOOK"]
ALERT_MIDDLE_CHANNEL_WEBHOOK = secret["ALERT_MIDDLE_CHANNEL_WEBHOOK"]
USERGROUP_ID = secret["USERGROUP_ID"]


def notify_error(event, context):
    logger.info(event["Execution"])
    logger.info(event["State"])
    logger.info(event["StateMachine"])
    # StepFunctions の 前のステップから情報取得
    error = event["param"]["Error"]
    cause = event["param"]["Cause"]

    # StepFunctions の Context オブジェクトの情報取得
    input = event["Execution"]["Input"]
    execution_arn = event["Execution"]["Id"]
    execution_arn_regex = "arn:aws:states:(.*):([0-9]{12}):execution:(.*):(.*)"

    # Context オブジェクトの情報をパース
    region = re.search(execution_arn_regex, execution_arn).group(1)
    account_id = re.search(execution_arn_regex, execution_arn).group(2)
    sfn_machine_name = re.search(execution_arn_regex, execution_arn).group(3)

    execution_url = f"https://{region}.console.aws.amazon.com/states/home?region={region}#/executions/details/{execution_arn}"

    # Slackに投稿するメッセージ作成
    title = (
        f"StepFunctions Alert | {sfn_machine_name} | {region} | Account:{account_id}"
    )

    title_link = f"{execution_url}"

    from_time = event["Execution"]["StartTime"]

    # エラー原因に応じて通知種類を変更
    if "Task timed outss" in cause:
        alert_middle(title, title_link, error, cause, from_time, input)
    else:
        alert_high(title, title_link, error, cause, from_time, input)


def alert_middle(title, title_link, error, cause, from_time, input):
    title = ":warning: " + title
    payload = {
        "attachments": [
            {
                "fallback": "Error test-alert-sls",
                "color": "warning",
                "title": title,
                "title_link": title_link,
                "fields": [
                    {"title": "Error", "value": error, "short": False},
                    {"title": "Cause", "value": cause, "short": False},
                    {"title": "From Time", "value": from_time, "short": False},
                    {"title": "Input", "value": f"```{input}```", "short": False},
                ],
            }
        ]
    }
    data = json.dumps(payload)
    try:
        requests.post(ALERT_MIDDLE_CHANNEL_WEBHOOK, data=data)
    except Exception as e:
        logger.exception("alert_middle {}".format(e))
        raise


def alert_high(title, title_link, error, cause, from_time, input):
    title = ":rotating_light: " + title
    usergroup_id = USERGROUP_ID
    payload = {
        "attachments": [
            {
                "fallback": "Error test-alert-sls",
                "pretext": f"<!subteam^{usergroup_id}>",
                "color": "danger",
                "title": title,
                "title_link": title_link,
                "fields": [
                    {"title": "Error", "value": error, "short": False},
                    {"title": "Cause", "value": cause, "short": False},
                    {"title": "From Time", "value": from_time, "short": False},
                    {"title": "Input", "value": f"```{input}```", "short": False},
                ],
            }
        ]
    }
    data = json.dumps(payload)
    try:
        requests.post(ALERT_HIGH_CHANNEL_WEBHOOK, data=data)
    except Exception as e:
        logger.exception("alert_high {}".format(e))
        raise
