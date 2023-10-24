import logging

from flask import Blueprint

logger = logging.getLogger(__name__)

zid_bp = Blueprint("zid_bp", __name__)

from . import routes
