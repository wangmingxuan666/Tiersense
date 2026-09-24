"""Minimal hosted API client. No model routing, compression or retrieval execution."""
import argparse
import json
import os
from pathlib import Path
import sys
import urllib.error
import urllib.request

ENDPOINTS = {
    "score": "https://tierflow.cn/tiersense/v1/score",
    "compress": "https://tierflow.cn/tiersense/v1/compress",
    "memory-decide": "https://tierflow.cn/tiersense/v1/memory/decide",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("module", choices=ENDPOINTS)
    parser.add_argument("--input", required=True, type=Path, help="JSON request body")
    args = parser.parse_args()
    key = os.environ.get("TIERSENSE_API_KEY")
    if not key:
        parser.error("Set TIERSENSE_API_KEY in your environment.")
    body = json.loads(args.input.read_text(encoding="utf-8"))
    request = urllib.request.Request(
        ENDPOINTS[args.module],
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            result = json.load(response)
    except urllib.error.HTTPError as error:
        print(f"HTTP {error.code}: request failed; no decision produced.", file=sys.stderr)
        return 1
    except urllib.error.URLError as error:
        print(f"Transport error: {error.reason}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
