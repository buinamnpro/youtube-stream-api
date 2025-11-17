import os
import uuid
import tempfile
import shutil
import yt_dlp
import requests
from flask import Flask, request, Response, jsonify, url_for

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
STREAM_TOKENS = {}

# --- TÌM KIẾM VIDEO ---
def search_youtube_and_get_url(query):
    ydl_opts = {
        'default_search': 'ytsearch1',
        'quiet': True,
        'format': 'bestaudio',
        'skip_download': True
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            if info and 'entries' in info and len(info['entries']) > 0:
                return info['entries'][0].get('webpage_url')
            return None
    except Exception as e:
        print(f"LỖI TÌM KIẾM YOUTUBE: {e}")
        return None


def fetch_basic_info(youtube_url):
    info_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'skip_download': True,
    }

    try:
        with yt_dlp.YoutubeDL(info_opts) as ydl:
            return ydl.extract_info(youtube_url, download=False)
    except Exception as e:
        print("LỖI LẤY THÔNG TIN:", e)
        return None


def download_mp3_to_temp(youtube_url):
    temp_dir = tempfile.mkdtemp(prefix="ytmp3_", dir=DOWNLOAD_DIR)
    outtmpl = os.path.join(temp_dir, '%(id)s.%(ext)s')

    download_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'outtmpl': outtmpl,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            'nopostoverwrites': False,
        }],
        'postprocessor_args': [
            '-ar', '24000',
            '-ac', '2'
        ],
        'keepvideo': False,
        'overwrites': True,
        'ffmpeg_location': r'C:\ProgramData\chocolatey\bin',
    }

    try:
        with yt_dlp.YoutubeDL(download_opts) as ydl:
            ydl.download([youtube_url])
    except Exception as e:
        print("LỖI TẢI/XUẤT MP3:", e)
        shutil.rmtree(temp_dir, ignore_errors=True)
        return None, None

    for filename in os.listdir(temp_dir):
        if filename.endswith(".mp3"):
            return os.path.join(temp_dir, filename), temp_dir

    shutil.rmtree(temp_dir, ignore_errors=True)
    return None, None


# --- API TRẢ VỀ URL ---
@app.route('/get_audio_url', methods=['GET'])
def get_audio_url():
    """
    Endpoint dành cho firmware Xiaozhi:
    - Cho phép truyền ?q=<tên bài hát> hoặc ?url=<youtube link>
    - Trả về JSON chứa URL audio trực tiếp để ESP32 stream.
    """
    youtube_url = request.args.get('url')
    query = request.args.get('q')

    if query:
        print("Nhận yêu cầu tìm kiếm:", query)
        youtube_url = search_youtube_and_get_url(query)
        if not youtube_url:
            return jsonify({"error": f"Không tìm thấy video cho từ khóa: {query}"}), 404
        print("URL tìm được:", youtube_url)

    if not youtube_url:
        return jsonify({"error": "Thiếu tham số 'url' hoặc 'q'"}), 400

    info = fetch_basic_info(youtube_url)
    title = info.get('title', 'Audio Stream Link') if info else 'Audio Stream Link'
    artist = info.get('uploader', '') if info else ''

    token = uuid.uuid4().hex
    STREAM_TOKENS[token] = {
        "youtube_url": youtube_url,
        "title": title,
        "artist": artist
    }

    audio_url = request.host_url.rstrip('/') + url_for('stream_mp3_token', token=token)

    return jsonify({
        "status": "success",
        "title": title or "Audio Stream Link",
        "audio_url": audio_url,
        "content_type": "audio/mpeg",
        "artist": artist,
        "lyric_url": ""
    })


# --- API STREAM (TÙY CHỌN) ---
@app.route('/stream', methods=['GET'])
def stream_audio():
    youtube_url = request.args.get('url')
    query = request.args.get('q')

    if query:
        print("Nhận yêu cầu tìm kiếm:", query)
        youtube_url = search_youtube_and_get_url(query)
        if not youtube_url:
            return {"error": "Không tìm thấy video"}, 404
        print("URL tìm được:", youtube_url)

    if not youtube_url:
        return {"error": "Thiếu url hoặc q"}, 400

    def generate():
        print("-> Bắt đầu stream MP3 tạm thời...")
        mp3_path, temp_dir = download_mp3_to_temp(youtube_url)
        if not mp3_path:
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

    return Response(generate(), content_type="audio/mpeg")


@app.route('/stream_mp3/<token>')
def stream_mp3_token(token):
    entry = STREAM_TOKENS.pop(token, None)
    if not entry:
        return {"error": "Token không hợp lệ hoặc đã hết hạn"}, 404

    youtube_url = entry["youtube_url"]

    def generate():
        print(f"-> Bắt đầu chuyển đổi tạm MP3 cho token {token}")
        mp3_path, temp_dir = download_mp3_to_temp(youtube_url)
        if not mp3_path:
            print("-> Không thể tạo MP3 tạm thời")
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

    return Response(generate(), content_type="audio/mpeg")


# --- CHẠY SERVER ---
if __name__ == "__main__":
    HOST = "0.0.0.0"
    PORT = 5000

    print("==============================================")
    print(" SERVER ĐÃ KHỞI ĐỘNG ")
    print(" Truy cập trên laptop:")
    print(f"   http://127.0.0.1:{PORT}/stream?q=nhac")
    print("")
    print(" Truy cập bằng ĐIỆN THOẠI (cùng WiFi):")
    print(f"   http://<IP-LAPTOP>:{PORT}/stream?q=nhac")
    print("==============================================")

    app.run(host=HOST, port=PORT, debug=False)
