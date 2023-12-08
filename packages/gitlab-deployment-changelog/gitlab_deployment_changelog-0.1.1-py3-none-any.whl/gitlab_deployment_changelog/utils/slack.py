import requests
from decouple import config
from loguru import logger

WEBHOOK_URL = config('WEBHOOK_URL', cast=str, default="")


def send_to_slack(msg: str) -> None:
    if not WEBHOOK_URL:
        logger.warning('no WEBHOOK_URL configured')
        logger.info(msg)
        return
    jsons = {
        "text": msg
    }
    try:
        logger.info(f"To Slack: {msg}")
        ret = requests.post(WEBHOOK_URL, json=jsons)
        logger.debug(f"Slack returned status code {ret.status_code}")
        logger.debug(f"Slack returned '{ret.text}'")
    except requests.exceptions.SSLError as ex:
        logger.error('SSL Error, could not send slack msg')
        logger.error(ex)
    except Exception as ex:
        logger.error('Other exception;')
        logger.error(ex)
    return
