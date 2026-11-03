import hashlib
import json

def generate_request_hash(payload: dict) -> str:
    content = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )

    return hashlib.sha256(content.encode("utf-8")).hexdigest()