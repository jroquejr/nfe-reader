from datetime import datetime

from flask import Blueprint, request

from nfe_reader import UF_CRAWLERS

blueprint = Blueprint("api", __name__)


@blueprint.route("/healthcheck", methods=("GET",))
def healthcheck():
    return {"status": True, "now": datetime.now()}


@blueprint.route("/", methods=("POST",))
def nfe_reader():
    url_qrcode = request.json.get("url_qrcode")

    if not url_qrcode:
        return {"message": "Missing URL QRCODE"}, 400

    try:
        crawler = UF_CRAWLERS.get("ba")()
        result = crawler.search_by_qrcode(url_qrcode)
    except Exception:
        return {"message": "Couldnt read the URL"}, 500

    return {"data": result.to_primitive()}
