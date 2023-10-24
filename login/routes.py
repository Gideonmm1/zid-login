import logging

from flask import jsonify, redirect, request

from .helper import (
    generate_login_url,
    get_authorization,
    get_credentials,
    refresh_token,
)

from . import zid_bp

logger = logging.getLogger(__name__)


@zid_bp.route("/", methods=["GET"])
def home():
    return jsonify(success=True)


@zid_bp.route("/login", methods=["GET"])
def login():
    logger.debug("Initiating authorization process")
    url = generate_login_url()
    logger.debug("Redirecting user to login page")
    print(url)
    return redirect(url)


@zid_bp.route("/callback", methods=["GET"])
def zid_webhook():
    isSuccess = False
    args = request.args
    auth_code = args.get("code")
    if auth_code:
        isSuccess = get_authorization(auth_code)

    return redirect(f"/zid/status?status={isSuccess}")


@zid_bp.route("/status", methods=["GET"])
def status():
    args = request.args
    isSuccess = args.get("status") == "True"
    return jsonify(success=isSuccess)


@zid_bp.route("/refresh-token", methods=["GET"])
def refresh():
    is_success = refresh_token()
    if is_success:
        get_credentials(refresh=True)
    return jsonify(success=is_success)
