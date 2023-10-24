import json
import logging
import os
from urllib.parse import urlencode

import requests

logger = logging.getLogger(__name__)


def load_json(filename):
    try:
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        with open(file_path, "r") as file:
            return json.load(file)
    except Exception as e:
        raise e


def write_json(filename, data):
    try:
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        raise e


def get_authorization(access_code):
    response_status = False
    logger.info("Obtaining authorization code from ZID")
    try:
        url = "https://oauth.zid.sa/oauth/token"

        data = load_json("zid.json")
        payload = json.dumps(
            {
                "code": access_code,
                "grant_type": "authorization_code",
                "client_id": data.get("client_id"),
                "client_secret": data.get("client_secret"),
                "redirect_uri": data.get("redirect_uri"),
            }
        )
        headers = {"Content-Type": "application/json"}

        response = requests.request("POST", url, headers=headers, data=payload)
        data = response.json()
        if response.status_code == 200 and "access_token" in data.keys():
            response_status = True
            logger.info("Obtained code from ZID")
            write_json("credentials.json", data)
    except Exception as e:
        logger.error(f"Could not fetch authorization token: {e}")

    return response_status


def get_credentials(refresh=False):
    logger.debug("Fetching Zid API credentials")
    if refresh or not hasattr(get_credentials, "cached_data"):
        data = load_json("credentials.json")
        get_credentials.cached_data = data
    return get_credentials.cached_data


def generate_login_url():
    data = load_json("zid.json")
    params = {
        "client_id": data.get("client_id"),
        "redirect_uri": data.get("redirect_uri"),
        "response_type": "code",
    }
    url = "https://oauth.zid.sa/oauth/authorize?"
    url = url + urlencode(params)
    return url


def refresh_token():
    is_success = False
    try:
        url = "https://oauth.zid.sa/oauth/token"
        logger.debug("Refreshing zid token")

        data = load_json("zid.json")
        creds = load_json("credentials.json")

        payload = json.dumps(
            {
                "grant_type": "refresh_token",
                "refresh_token": creds.get("refresh_token"),
                "client_id": data.get("client_id"),
                "client_secret": data.get("client_secret"),
                "redirect_uri": data.get("redirect_uri"),
            }
        )
        headers = {"Content-Type": "application/json"}

        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code == 200:
            logger.info("Token refreshed")
            data = response.json()
            is_success = True
            write_json("credentials.json", data)
        elif response.status_code == 400:
            data = response.json()
            error_code = data.get("message", {}).get("code", "")
            logger.error(f"Error refreshing token: {error_code}")
            logger.error(response.json())
        else:
            logger.error(response.status_code)
            logger.error("Error refreshing token")
            logger.error(response.json())
    except Exception as e:
        logger.error(f"Could not refresh zid token: {e}")
    return is_success
