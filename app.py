import os
import uuid
import tempfile
import shutil

import yt_dlp
from flask import Flask, request, Response, jsonify, url_for

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
STREAM_TOKENS = {}


def search_soundcloud_url(query):
    """Tìm kiếm SoundCloud và trả về URL track đầu tiên."""
    search_prefix = "scsearch1:"
    if not query.startswith(search_prefix):
        query = search_prefix + query

    ydl_opts = {
        "default_search": search_prefix,
        "quiet": True,
        "format": "bestaudio",
        "skip_download": True,
        "user_agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"
        ),
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            entries = info.get("entries") if info else []
            if entries:
                return entries[0].get("webpage_url")
    except Exception as exc:
        print(f"LỖI TÌM KIẾM SOUNDCLOUD: {exc}")
    return None


def fetch_basic_info(track_url):
    """Lấy metadata cơ bản để trả về cho firmware."""
    info_opts = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "quiet": True,
        "skip_download": True,
    }
    try:
        with yt_dlp.YoutubeDL(info_opts) as ydl:
            return ydl.extract_info(track_url, download=False)
    except Exception as exc:
        print(f"LỖI LẤY THÔNG TIN TRACK: {exc}")
    return None


def download_and_convert_to_mp3(track_url):
    """Tải audio và chuyển sang MP3 bằng FFmpeg."""
    temp_dir = tempfile.mkdtemp(prefix="scmp3_", dir=DOWNLOAD_DIR)
    outtmpl = os.path.join(temp_dir, "%(id)s.%(ext)s")

    download_opts = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "quiet": True,
        "outtmpl": outtmpl,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
            "nopostoverwrites": False,
        }],
        "postprocessor_args": [
            "-ar", "24000",
            "-ac", "2",
        ],
        "keepvideo": False,
        "overwrites": True,
    }

    print(f"-> Bắt đầu TẢI & CHUYỂN MP3: {track_url}")
    try:
        with yt_dlp.YoutubeDL(download_opts) as ydl:
            ydl.download([track_url])
    except Exception as exc:
        print(f"LỖI TẢI/XUẤT MP3: {exc}")
        shutil.rmtree(temp_dir, ignore_errors=True)
        return None, None

    for filename in os.listdir(temp_dir):
        if filename.endswith(".mp3"):
            return os.path.join(temp_dir, filename), temp_dir

    shutil.rmtree(temp_dir, ignore_errors=True)
    return None, None


@app.route("/get_audio_url", methods=["GET"])
def get_audio_url():
    track_url = request.args.get("url")
    query = request.args.get("q")

    if query:
        print("Nhận yêu cầu tìm kiếm SoundCloud:", query)
        track_url = search_soundcloud_url(query)
        if not track_url:
            return jsonify({
                "error": f"Không tìm thấy track SoundCloud cho từ khóa: {query}"
            }), 404
        print("URL SoundCloud tìm được:", track_url)

    if not track_url:
        return jsonify({"error": "Thiếu tham số 'url' hoặc 'q'"}), 400

    info = fetch_basic_info(track_url)
    title = info.get("title", "SoundCloud Stream") if info else "SoundCloud Stream"
    artist = info.get("uploader", "") if info else ""

    token = uuid.uuid4().hex
    STREAM_TOKENS[token] = {
        "track_url": track_url,
        "title": title,
        "artist": artist,
    }

    audio_url = request.host_url.rstrip("/") + url_for("stream_mp3_token", token=token)

    return jsonify({
        "status": "success",
        "title": title,
        "audio_url": audio_url,
        "content_type": "audio/mpeg",
        "artist": artist,
        "lyric_url": "",
    })


@app.route("/stream", methods=["GET"])
def stream_audio():
    track_url = request.args.get("url")
    query = request.args.get("q")

    if query:
        print("Nhận yêu cầu tìm kiếm SoundCloud:", query)
        track_url = search_soundcloud_url(query)
        if not track_url:
            return jsonify({
                "error": f"Không tìm thấy track SoundCloud cho từ khóa: {query}"
            }), 404
        print("URL SoundCloud tìm được:", track_url)

    if not track_url:
        return jsonify({"error": "Thiếu url hoặc q"}), 400

    mp3_path, temp_dir = download_and_convert_to_mp3(track_url)
    if not mp3_path:
        return jsonify({"error": "Không thể tạo file MP3 (kiểm tra FFmpeg)."}), 500

    def generate():
        print(f"-> STREAM MP3 từ file: {mp3_path}")
        try:
            with open(mp3_path, "rb") as f:
                while True:
                    chunk = f.read(8192)
                    if not chunk:
                        break
                    yield chunk
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
            print("-> Đã dọn dẹp file MP3 tạm.")

    return Response(generate(), content_type="audio/mpeg")


@app.route("/stream_mp3/<token>")
def stream_mp3_token(token):
    entry = STREAM_TOKENS.pop(token, None)
    if not entry:
        return jsonify({"error": "Token không hợp lệ hoặc đã hết hạn"}), 404

    track_url = entry["track_url"]

    def generate():
        print(f"-> Bắt đầu convert MP3 cho token {token}")
        mp3_path, temp_dir = download_and_convert_to_mp3(track_url)
        if not mp3_path:
            print("-> Không thể tạo MP3 tạm thời cho token")
            yield b""
            return
        try:
            with open(mp3_path, "rb") as f:
                while True:
                    chunk = f.read(8192)
                    if not chunk:
                        break
                    yield chunk
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
            print(f"-> Đã dọn dẹp token {token}")

    resp = Response(generate(), content_type="audio/mpeg")
    resp.headers["Accept-Ranges"] = "bytes"
    resp.headers["Cache-Control"] = "no-cache"
    return resp


if __name__ == "__main__":
    HOST = os.environ.get("HOST", "0.0.0.0")
    PORT = int(os.environ.get("PORT", 5000))

    print("=====================================================")
    print(" SERVER SOUNDCLOUD MP3 STREAM (CẦN FFmpeg) ĐÃ SẴN SÀNG ")
    print("=====================================================")

    app.run(host=HOST, port=PORT, debug=False)
