#!/usr/bin/env python3
"""
Bản 3 không-cookies:
- KHÔNG sử dụng cookiefile
- KHÔNG đọc YOUTUBE_COOKIES
- Không ép player_client
- Giữ hành vi yt-dlp mặc định để tránh bot-detection
"""

import os
import time
import uuid
import tempfile
import shutil
import random
import yt_dlp
from flask import Flask, request, Response, jsonify, url_for

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

STREAM_TOKENS = {}

# Tạo rate limiter đơn giản tránh spam YouTube
_RATE_LIMIT = {
    "search": {"last": 0.0, "min_interval": 0.6},
    "download": {"last": 0.0, "min_interval": 0.4},
}

def _maybe_rate_limit(kind):
    info = _RATE_LIMIT.get(kind)
    if not info:
        return
    now = time.time()
    wait = info["min_interval"] - (now - info["last"])
    if wait > 0:
        time.sleep(wait + random.uniform(0, 0.1))
    info["last"] = time.time()

# ---------------------------------------------
# SEARCH YOUTUBE (không cookies, không header hack)
# ---------------------------------------------
def search_youtube_and_get_url(query, retries=2):
    if not query:
        return None

    _maybe_rate_limit("search")

    search_query = f"ytsearch1:{query}"

    ydl_opts = {
        "default_search": "ytsearch1",
        "quiet": True,
        "skip_download": True,
    }

    attempt = 0
    while attempt <= retries:
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(search_query, download=False)
                if not info:
                    return None

                entries = info.get("entries") or []
                entries = [e for e in entries if e]

                if not entries:
                    return None

                entry = entries[0]

                url = entry.get("webpage_url") or entry.get("url")
                if not url and entry.get("id"):
                    url = f"https://www.youtube.com/watch?v={entry['id']}"

                if not url:
                    return None

                title = entry.get("title") or ""
                artist = entry.get("uploader") or entry.get("channel") or ""

                if title or artist:
                    return {"url": url, "title": title, "artist": artist}

                return url

        except Exception:
            attempt += 1
            if attempt > retries:
                return None
            time.sleep(0.4 + random.uniform(0, 0.2))

    return None

# ---------------------------------------------
# FETCH BASIC INFO
# ---------------------------------------------
def fetch_basic_info(url):
    if not url:
        return None

    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "skip_download": True,
        "noplaylist": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download=False)
    except Exception:
        return None

# ---------------------------------------------
# DOWNLOAD MP3 (Không cookies)
# ---------------------------------------------
def download_mp3_to_temp(url, retries=2):
    if not url:
        return None, None

    _maybe_rate_limit("download")

    temp_dir = tempfile.mkdtemp(prefix="ytmp3_", dir=DOWNLOAD_DIR)
    outtmpl = os.path.join(temp_dir, "%(id)s.%(ext)s")

    download_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "noplaylist": True,
        "outtmpl": outtmpl,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "postprocessor_args": ["-ar", "24000", "-ac", "2"],
        "keepvideo": False,
    }

    attempt = 0
    while attempt <= retries:
        try:
            with yt_dlp.YoutubeDL(download_opts) as ydl:
                ydl.download([url])

            for fn in os.listdir(temp_dir):
                if fn.endswith(".mp3"):
                    return os.path.join(temp_dir, fn), temp_dir

            attempt += 1
        except Exception:
            attempt += 1

        time.sleep(0.4 + random.uniform(0, 0.3))

    shutil.rmtree(temp_dir, ignore_errors=True)
    return None, None

# ---------------------------------------------
# API GET URL
# ---------------------------------------------
@app.route("/get_audio_url")
def get_audio_url():
    url = request.args.get("url")
    query = request.args.get("q")

    title = ""
    artist = ""

    if query:
        result = search_youtube_and_get_url(query)
        if not result:
            return jsonify({"error": "Không tìm thấy video", "query": query}), 404

        if isinstance(result, dict):
            url = result["url"]
            title = result.get("title", "")
            artist = result.get("artist", "")
        else:
            url = result

    if not url:
        return jsonify({"error": "Thiếu url hoặc q"}), 400

    if not title:
        info = fetch_basic_info(url)
        if info:
            title = info.get("title", "")
            artist = info.get("uploader", "")

    token = uuid.uuid4().hex
    STREAM_TOKENS[token] = {"youtube_url": url, "title": title, "artist": artist}

    stream_url = request.host_url.rstrip("/") + url_for("stream_mp3_token", token=token)

    return jsonify({
        "status": "success",
        "title": title or "Audio Stream",
        "audio_url": stream_url,
        "artist": artist,
        "content_type": "audio/mpeg",
        "lyric_url": ""
    })

# ---------------------------------------------
# STREAM API
# ---------------------------------------------
@app.route("/stream")
def stream_audio():
    url = request.args.get("url")
    query = request.args.get("q")

    if query:
        result = search_youtube_and_get_url(query)
        if isinstance(result, dict):
            url = result["url"]
        else:
            url = result

    if not url:
        return jsonify({"error": "Thiếu url hoặc q"}), 400

    def generate():
        mp3_path, temp_dir = download_mp3_to_temp(url)
        if not mp3_path:
            yield b""
            return

        try:
            with open(mp3_path, "rb") as f:
                while chunk := f.read(8192):
                    yield chunk
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    return Response(generate(), content_type="audio/mpeg")

@app.route("/stream_mp3/<token>")
def stream_mp3_token(token):
    entry = STREAM_TOKENS.pop(token, None)
    if not entry:
        return jsonify({"error": "Token hết hạn hoặc sai"}), 404

    url = entry["youtube_url"]

    def generate():
        mp3_path, temp_dir = download_mp3_to_temp(url)
        if not mp3_path:
            yield b""
            return

        try:
            with open(mp3_path, "rb") as f:
                while chunk := f.read(8192):
                    yield chunk
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    resp = Response(generate(), content_type="audio/mpeg")
    resp.headers["Accept-Ranges"] = "bytes"
    resp.headers["Cache-Control"] = "no-cache"
    return resp

# ---------------------------------------------
# RUN SERVER
# ---------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
