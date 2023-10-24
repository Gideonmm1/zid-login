import logging

from flask import Flask

from login import zid_bp

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.register_blueprint(zid_bp, url_prefix="/zid")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
