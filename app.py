import os
import uuid
import tempfile
import shutil
import urllib.parse
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
    # Decode URL encoding nếu có
    if query:
        query = urllib.parse.unquote_plus(query)
    
    # Format query để yt-dlp nhận diện là YouTube search
    # Phải có prefix "ytsearch1:" để yt-dlp biết đây là YouTube search
    search_query = f"ytsearch1:{query}"
    
    # Cấu hình để tránh bot detection - dùng extract_flat để chỉ lấy URL
    ydl_opts = {
        'quiet': False,
        'format': 'bestaudio',
        'skip_download': True,
        'extract_flat': 'in_playlist',  # Chỉ extract flat cho playlist, không cho video (để có metadata)
        # Thêm headers để tránh bot detection
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        },
        # Retry với delay
        'retries': 3,
        'fragment_retries': 3,
        'ignoreerrors': True,  # Bỏ qua lỗi để tiếp tục
        # Thêm options để tránh rate limit
        'sleep_interval': 1,
        'max_sleep_interval': 5,
        # Extractor args - chỉ dùng android client
        'extractor_args': {
            'youtube': {
                'player_client': ['android'],  # Chỉ dùng android, ít bị block hơn
                'player_skip': ['webpage', 'configs'],
            }
        },
    }
    
    # Sử dụng cookies từ file hoặc environment variable
    cookies_file = os.path.join(BASE_DIR, 'cookies.txt')
    cookies_from_env = os.environ.get('YOUTUBE_COOKIES')
    
    if os.path.exists(cookies_file):
        ydl_opts['cookiefile'] = cookies_file
        print(f"🍪 Sử dụng cookies từ file cho tìm kiếm")
    elif cookies_from_env:
        # Tạo file cookies từ environment variable
        temp_cookies_file = os.path.join(BASE_DIR, 'cookies_env.txt')
        try:
            with open(temp_cookies_file, 'w') as f:
                f.write(cookies_from_env)
            ydl_opts['cookiefile'] = temp_cookies_file
            print(f"🍪 Sử dụng cookies từ env cho tìm kiếm")
        except Exception as e:
            print(f"⚠️ Không thể tạo cookies từ env: {e}")
    
    import time
    max_retries = 3
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            print(f"🔍 Đang tìm kiếm (lần {attempt + 1}/{max_retries}): '{query}'")
            print(f"🔍 Query formatted: '{search_query}'")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(search_query, download=False)
                print(f"📊 Kết quả tìm kiếm type: {type(info)}")
                print(f"📊 Kết quả có entries?: {'entries' in info if info else 'None'}")
                
                if info and 'entries' in info:
                    entries = [e for e in info['entries'] if e]  # Loại bỏ None entries
                    print(f"📊 Số lượng entries: {len(entries)}")
                    if len(entries) > 0:
                        entry = entries[0]
                        # Debug: In ra cấu trúc entry để xem có gì
                        print(f"📋 Entry type: {type(entry)}")
                        print(f"📋 Entry keys: {list(entry.keys()) if entry and isinstance(entry, dict) else 'Not a dict'}")
                        if entry and isinstance(entry, dict):
                            print(f"📋 Entry có 'id'?: {'id' in entry}")
                            print(f"📋 Entry có 'url'?: {'url' in entry}")
                            print(f"📋 Entry có 'webpage_url'?: {'webpage_url' in entry}")
                        
                        # Với extract_flat=True, có thể chỉ có id, cần build URL
                        video_id = entry.get('id')
                        if video_id:
                            video_url = f"https://www.youtube.com/watch?v={video_id}"
                            print(f"✅ Tìm thấy video ID: {video_id}")
                            print(f"✅ URL: {video_url}")
                            # Lưu metadata từ entry nếu có (tránh phải lấy lại sau)
                            if 'title' in entry or 'uploader' in entry:
                                return {
                                    'url': video_url,
                                    'title': entry.get('title', ''),
                                    'artist': entry.get('uploader', entry.get('channel', '')),
                                }
                            return video_url
                        
                        # Hoặc có sẵn URL
                        video_url = entry.get('webpage_url') or entry.get('url')
                        if video_url:
                            print(f"✅ Tìm thấy video URL: {video_url}")
                            # Extract ID từ URL nếu cần
                            import re
                            id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11})', video_url)
                            if id_match:
                                print(f"✅ Video ID từ URL: {id_match.group(1)}")
                            # Lưu metadata từ entry nếu có
                            if 'title' in entry or 'uploader' in entry:
                                return {
                                    'url': video_url,
                                    'title': entry.get('title', ''),
                                    'artist': entry.get('uploader', entry.get('channel', '')),
                                }
                            return video_url
                        
                        # Nếu không có cả ID và URL
                        print(f"⚠️ Entry không có 'id' hoặc 'url': {entry}")
                    else:
                        print("⚠️ Không có entries hợp lệ")
                else:
                    print("⚠️ Không có entries trong kết quả")
                return None
        except Exception as e:
            error_msg = str(e)
            print(f"❌ LỖI TÌM KIẾM YOUTUBE (lần {attempt + 1}): {error_msg}")
            
            # Nếu là lỗi bot detection, thử lại với delay
            if "bot" in error_msg.lower() or "precondition" in error_msg.lower() or "400" in error_msg:
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (attempt + 1)
                    print(f"⏳ Đợi {wait_time} giây trước khi thử lại...")
                    time.sleep(wait_time)
                    continue
                else:
                    print("❌ Đã thử tất cả các lần, YouTube có thể đang block")
                    return None
            else:
                # Lỗi khác, không retry
                import traceback
                print(traceback.format_exc())
                return None
    
    return None


def fetch_basic_info(youtube_url):
    # Thử lấy thông tin, nhưng nếu bị block thì dùng giá trị mặc định
    # Dùng extract_flat để tránh bot detection khi lấy metadata
    info_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': False,
        'skip_download': True,
        'ignoreerrors': True,  # Bỏ qua lỗi
        'extract_flat': True,  # Chỉ lấy URL, không cần metadata (tránh bot detection)
        # Thêm headers để tránh bot detection
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
        },
        'retries': 1,  # Giảm retry để nhanh hơn
        'fragment_retries': 1,
        'extractor_args': {
            'youtube': {
                'player_client': ['android'],  # Chỉ dùng android
            }
        },
    }
    
    # Sử dụng cookies từ file hoặc environment variable
    cookies_file = os.path.join(BASE_DIR, 'cookies.txt')
    cookies_from_env = os.environ.get('YOUTUBE_COOKIES')
    
    if os.path.exists(cookies_file):
        info_opts['cookiefile'] = cookies_file
    elif cookies_from_env:
        temp_cookies_file = os.path.join(BASE_DIR, 'cookies_env.txt')
        try:
            with open(temp_cookies_file, 'w') as f:
                f.write(cookies_from_env)
            info_opts['cookiefile'] = temp_cookies_file
        except:
            pass

    try:
        with yt_dlp.YoutubeDL(info_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            # Nếu bị block, info có thể None hoặc thiếu dữ liệu
            if info:
                return info
            else:
                print("⚠️ Không lấy được thông tin, dùng giá trị mặc định")
                return None
    except Exception as e:
        error_msg = str(e)
        # Nếu là lỗi bot, không cần retry - đây là điều bình thường
        if "bot" in error_msg.lower() or "login" in error_msg.lower():
            print(f"⚠️ YouTube yêu cầu xác thực (bình thường), dùng giá trị mặc định")
            print(f"   Chi tiết: {error_msg[:150]}")
        else:
            print(f"⚠️ LỖI LẤY THÔNG TIN: {error_msg[:150]}")
        return None


def download_mp3_to_temp(youtube_url):
    print(f"📥 Bắt đầu tải video: {youtube_url}")
    temp_dir = tempfile.mkdtemp(prefix="ytmp3_", dir=DOWNLOAD_DIR)
    outtmpl = os.path.join(temp_dir, '%(id)s.%(ext)s')

    download_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': False,
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
        # Thêm headers để tránh bot detection
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        },
        'retries': 3,
        'fragment_retries': 3,
        'ignoreerrors': True,  # Bỏ qua lỗi để tiếp tục
        'extractor_args': {
            'youtube': {
                'player_client': ['android'],  # Chỉ dùng android, ít bị block
            }
        },
    }
    
    # Sử dụng cookies từ file hoặc environment variable
    cookies_file = os.path.join(BASE_DIR, 'cookies.txt')
    cookies_from_env = os.environ.get('YOUTUBE_COOKIES')
    
    if os.path.exists(cookies_file):
        download_opts['cookiefile'] = cookies_file
        print(f"🍪 Sử dụng cookies từ file: {cookies_file}")
    elif cookies_from_env:
        # Tạo file cookies từ environment variable
        temp_cookies_file = os.path.join(BASE_DIR, 'cookies_env.txt')
        try:
            with open(temp_cookies_file, 'w') as f:
                f.write(cookies_from_env)
            download_opts['cookiefile'] = temp_cookies_file
            print(f"🍪 Sử dụng cookies từ environment variable")
        except Exception as e:
            print(f"⚠️ Không thể tạo cookies từ env: {e}")
    else:
        print(f"⚠️ Không tìm thấy cookies.txt, có thể bị block")
        print(f"   Tạo file cookies.txt hoặc set YOUTUBE_COOKIES env (xem COOKIES_GUIDE.md)")
    
    # Chỉ set ffmpeg_location nếu có biến môi trường (cho Windows local)
    ffmpeg_path = os.environ.get('FFMPEG_PATH')
    if ffmpeg_path:
        download_opts['ffmpeg_location'] = ffmpeg_path

    try:
        print(f"📥 Đang tải và chuyển đổi sang MP3...")
        with yt_dlp.YoutubeDL(download_opts) as ydl:
            ydl.download([youtube_url])
        print(f"✅ Tải và chuyển đổi thành công!")
    except Exception as e:
        error_msg = str(e)
        print(f"❌ LỖI TẢI/XUẤT MP3: {error_msg}")
        import traceback
        print(traceback.format_exc())
        shutil.rmtree(temp_dir, ignore_errors=True)
        return None, None

    # Tìm file MP3 đã tạo
    print(f"🔍 Đang tìm file MP3 trong: {temp_dir}")
    for filename in os.listdir(temp_dir):
        if filename.endswith(".mp3"):
            mp3_path = os.path.join(temp_dir, filename)
            file_size = os.path.getsize(mp3_path)
            print(f"✅ Tìm thấy file MP3: {filename} ({file_size} bytes)")
            return mp3_path, temp_dir

    print(f"⚠️ Không tìm thấy file MP3 trong {temp_dir}")
    print(f"📋 Files trong thư mục: {os.listdir(temp_dir)}")
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
        # Decode URL encoding
        query = urllib.parse.unquote_plus(query)
        print(f"📥 Nhận yêu cầu tìm kiếm: '{query}'")
        youtube_url = search_youtube_and_get_url(query)
        if not youtube_url:
            return jsonify({
                "error": f"Không tìm thấy video cho từ khóa: {query}",
                "suggestion": "Thử với từ khóa khác hoặc dùng URL YouTube trực tiếp"
            }), 404
        # Kiểm tra nếu search_youtube_and_get_url trả về dict (có metadata)
        if isinstance(youtube_url, dict):
            # Đã có metadata từ kết quả tìm kiếm
            search_result = youtube_url
            youtube_url = search_result['url']
            title = search_result.get('title', '') or 'Audio Stream Link'
            artist = search_result.get('artist', '') or 'YouTube'
            print(f"✅ Đã có metadata từ tìm kiếm: {title} - {artist}")
        else:
            print(f"✅ URL tìm được: {youtube_url}")

    if not youtube_url:
        return jsonify({"error": "Thiếu tham số 'url' hoặc 'q'"}), 400

    # Chỉ lấy metadata nếu chưa có từ tìm kiếm
    if 'title' not in locals() or not title or title == 'Audio Stream Link':
        info = fetch_basic_info(youtube_url)
        # Nếu không lấy được info (bị block), dùng giá trị mặc định
        if info:
            title = info.get('title', 'Audio Stream Link') or 'Audio Stream Link'
            artist = info.get('uploader', '') or ''
        else:
            # Extract video ID từ URL để làm title
            import re
            video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', youtube_url)
            if video_id_match:
                video_id = video_id_match.group(1)
                title = f"YouTube Video {video_id}"
            else:
                title = 'Audio Stream Link'
            artist = 'YouTube'

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
        # Decode URL encoding
        query = urllib.parse.unquote_plus(query)
        print(f"📥 Nhận yêu cầu tìm kiếm: '{query}'")
        youtube_url = search_youtube_and_get_url(query)
        if not youtube_url:
            return {"error": f"Không tìm thấy video cho: {query}"}, 404
        print(f"✅ URL tìm được: {youtube_url}")

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
    print(f"🎵 Nhận yêu cầu stream MP3 cho token: {token}")
    entry = STREAM_TOKENS.pop(token, None)
    if not entry:
        print(f"❌ Token không hợp lệ hoặc đã hết hạn: {token}")
        return jsonify({"error": "Token không hợp lệ hoặc đã hết hạn"}), 404

    youtube_url = entry["youtube_url"]
    title = entry.get("title", "Unknown")
    print(f"🎵 Stream video: {title}")
    print(f"🎵 YouTube URL: {youtube_url}")

    def generate():
        try:
            print(f"🔄 Bắt đầu chuyển đổi MP3 cho token {token}")
            mp3_path, temp_dir = download_mp3_to_temp(youtube_url)
            if not mp3_path:
                print(f"❌ Không thể tạo MP3 tạm thời cho token {token}")
                yield b""
                return
            
            print(f"✅ Đã tạo MP3, bắt đầu stream: {mp3_path}")
            file_size = os.path.getsize(mp3_path)
            print(f"📊 File size: {file_size} bytes")
            
            bytes_sent = 0
            with open(mp3_path, "rb") as f:
                while True:
                    chunk = f.read(8192)
                    if not chunk:
                        break
                    bytes_sent += len(chunk)
                    yield chunk
                    # Log tiến độ mỗi 1MB
                    if bytes_sent % (1024 * 1024) < 8192:
                        print(f"📤 Đã gửi: {bytes_sent}/{file_size} bytes ({bytes_sent*100//file_size}%)")
            
            print(f"✅ Hoàn thành stream MP3: {bytes_sent} bytes")
        except Exception as e:
            print(f"❌ LỖI KHI STREAM MP3: {e}")
            import traceback
            print(traceback.format_exc())
            yield b""
        finally:
            if 'temp_dir' in locals() and temp_dir:
                shutil.rmtree(temp_dir, ignore_errors=True)
                print(f"🧹 Đã dọn dẹp token {token}")

    response = Response(generate(), content_type="audio/mpeg")
    # Thêm headers để hỗ trợ streaming
    response.headers['Accept-Ranges'] = 'bytes'
    response.headers['Cache-Control'] = 'no-cache'
    return response


# --- CHẠY SERVER ---
if __name__ == "__main__":
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))

    print("==============================================")
    print(" SERVER ĐÃ KHỞI ĐỘNG ")
    print(" Truy cập trên laptop:")
    print(f"   http://127.0.0.1:{PORT}/stream?q=nhac")
    print("")
    print(" Truy cập bằng ĐIỆN THOẠI (cùng WiFi):")
    print(f"   http://<IP-LAPTOP>:{PORT}/stream?q=nhac")
    print("==============================================")

    app.run(host=HOST, port=PORT, debug=False)
