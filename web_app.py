#!/usr/bin/env python3
"""
Flask web app for Password Cracker Pro (educational simulation).

This web server exposes endpoints to start/stop a CPU-only demo cracking
process and a simple UI to control it.
"""

from __future__ import annotations

from flask import Flask, jsonify, render_template, request, send_file
import os
from werkzeug.exceptions import BadRequest

from web_cracker import PasswordCracker, CrackerConfig
from werkzeug.utils import secure_filename
import uuid


app = Flask(__name__)
cracker = PasswordCracker()

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'uploads')
ARTIFACTS_DIR = os.path.join(os.path.dirname(__file__), 'artifacts')
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(ARTIFACTS_DIR, exist_ok=True)


def _parse_config(data: dict) -> CrackerConfig:
    try:
        target_password = str(data.get("target_password", "1234"))
        method = str(data.get("method", "plain")).lower()
        password_length = int(data.get("password_length", 4))
        delay_seconds = float(data.get("delay_seconds", 0.01))
        charset = str(data.get("charset", "0123456789"))
    except Exception as exc:
        raise BadRequest(f"Invalid parameters: {exc}")

    if method not in ("plain", "md5", "sha256", "zip"):
        raise BadRequest("method must be one of: plain, md5, sha256, zip")

    # Guardrails to keep demo responsive and safe
    if not (1 <= password_length <= 6):
        raise BadRequest("password_length must be between 1 and 6 for demo")
    if len(charset) == 0 or len(set(charset)) != len(charset):
        raise BadRequest("charset must be a set of unique characters")
    if not (0.0 <= delay_seconds <= 1.0):
        raise BadRequest("delay_seconds must be between 0.0 and 1.0")

    return CrackerConfig(
        target_password=target_password,
        password_length=password_length,
        delay_seconds=delay_seconds,
        method=method,  # type: ignore[arg-type]
        charset=charset,
    )


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/status")
def api_status():
    return jsonify(cracker.status().to_dict())


@app.post("/api/start")
def api_start():
    if cracker.status().is_running:
        return jsonify({"error": "Cracker already running"}), 409
    body = request.get_json(silent=True) or {}
    cfg = _parse_config(body)
    if cfg.method == 'zip':
        token = body.get('zip_token')
        if not token:
            return jsonify({"error": "zip_token required for zip mode"}), 400
        zip_path = os.path.join(UPLOAD_DIR, secure_filename(str(token)))
        if not os.path.exists(zip_path):
            return jsonify({"error": "uploaded file not found"}), 400
        cfg.zip_path = zip_path
        cfg.job_id = str(uuid.uuid4())
        cfg.output_zip_path = os.path.join(ARTIFACTS_DIR, f"unlocked_{cfg.job_id}")
    cracker.start(cfg)
    return jsonify({"ok": True})


@app.post("/api/stop")
def api_stop():
    cracker.stop()
    return jsonify({"ok": True})


@app.post('/api/upload-zip')
def api_upload_zip():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    f = request.files['file']
    if f.filename == '':
        return jsonify({"error": "No selected file"}), 400
    filename = secure_filename(f.filename)
    token = str(uuid.uuid4()) + '_' + filename
    path = os.path.join(UPLOAD_DIR, token)
    f.save(path)
    return jsonify({"ok": True, "token": token})


@app.get('/api/download')
def api_download():
    s = cracker.status()
    if not s.artifact_path or not os.path.exists(s.artifact_path):
        return jsonify({"error": "No artifact available"}), 404
    return send_file(s.artifact_path, as_attachment=True)


def main():
    port = int(os.getenv("PORT", "5050"))
    app.run(host="127.0.0.1", port=port, debug=False)


if __name__ == "__main__":
    main()


