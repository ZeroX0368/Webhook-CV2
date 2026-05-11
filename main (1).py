from flask import Flask, request, jsonify
import requests
import time
from urllib.parse import quote

app = Flask(__name__)

NOPECHA_KEY = "weu64363hdhwzz97"
BYPASS_VIP_SITEKEY = "69a3b3f1-9884-4e4f-b381-2843c64d955d"
BYPASS_VIP_SITE = "https://bypass.vip"
BYPASS_API = "https://api.bypass.vip/bypass"

NOPECHA_HEADERS = {"Authorization": f"Basic {NOPECHA_KEY}"}


def solve_hcaptcha():
    try:
        resp = requests.post(
            "https://api.nopecha.com/v1/token/hcaptcha",
            headers={**NOPECHA_HEADERS, "Content-Type": "application/json"},
            json={"sitekey": BYPASS_VIP_SITEKEY, "url": BYPASS_VIP_SITE},
            timeout=15
        )
        data = resp.json()
    except Exception as e:
        return None, f"NopeCHA submit failed: {str(e)}"

    if data.get("error"):
        return None, f"NopeCHA error: {data.get('message', data)}"

    job_id = data.get("data")
    if not job_id:
        return None, f"No job ID returned: {data}"

    for _ in range(40):
        time.sleep(3)
        try:
            poll = requests.get(
                "https://api.nopecha.com/v1/token/hcaptcha",
                headers=NOPECHA_HEADERS,
                params={"id": job_id},
                timeout=15
            )
            poll_data = poll.json()
        except Exception as e:
            return None, f"NopeCHA poll failed: {str(e)}"

        error_code = poll_data.get("error")
        if error_code == 14:
            continue
        if error_code:
            return None, f"NopeCHA poll error {error_code}: {poll_data.get('message', poll_data)}"

        token = poll_data.get("data")
        if token and isinstance(token, str) and len(token) > 10:
            return token, None

    return None, "NopeCHA timed out solving hCaptcha"


def bypass_url(url):
    token, err = solve_hcaptcha()
    if err:
        return {"error": err}

    try:
        resp = requests.post(
            f"{BYPASS_API}?url={quote(url, safe='')}",
            headers={"Content-Type": "application/json"},
            json={"url": url, "hcaptchaToken": token},
            timeout=30
        )
        data = resp.json()
    except Exception as e:
        return {"error": f"Bypass request failed: {str(e)}"}

    if data.get("status") == "success":
        result_value = data.get("result")
        if isinstance(result_value, str):
            result_value = result_value.encode("utf-8").decode("unicode_escape")
        return {"status": "success", "result": result_value}

    return {"status": "error", "error": data.get("message", "Bypass failed"), "raw": data}


@app.route("/api/bypass", methods=["GET"])
def api_bypass():
    start_time = time.time()
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing 'url'"}), 400

    result = bypass_url(url)

    end_time = time.time()
    duration = f"{end_time - start_time:.2f}s"
    result["duration"] = duration

    if result.get("status") == "success":
        return jsonify(result)

    return jsonify(result), 500


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "Bypass API",
        "usage": "/api/bypass?url="
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
