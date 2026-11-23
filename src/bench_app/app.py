from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import hashlib
import inspect
import json
from urllib.parse import urlencode
import wirekit
from .signatures import sign_payload


def decode_response(response):
    content_type = response.headers.get("content-type", "application/json; charset=utf-8")
    charset = "utf-8"
    for parameter in content_type.split(";")[1:]:
        key, _, value = parameter.strip().partition("=")
        if key.lower() == "charset":
            charset = value.strip('"')
    return json.loads(response.body.decode(charset))


def retry_delay(value, now):
    try:
        return max(0, int(value))
    except ValueError:
        target = parsedate_to_datetime(value)
        return max(0, int((target - now).total_seconds()))


def run(request, root):
    deployment = json.loads((root / "context/deployment.json").read_text(encoding="utf-8"))
    if int(wirekit.__version__.split(".")[0]) != deployment["wire_major"]:
        raise ValueError("wirekit major does not match context/deployment.json")
    parameters = inspect.signature(wirekit.Client).parameters
    raise TypeError(f"wirekit.Client parameters: {parameters!r}")
