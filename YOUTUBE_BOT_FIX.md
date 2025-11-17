# 🔧 Fix YouTube Bot Detection

## Vấn Đề

YouTube đang block yt-dlp với lỗi:
- `ERROR - Precondition check failed`
- `HTTP Error 400: Bad Request`
- `Sign in to confirm you're not a bot`

## Giải Pháp Đã Áp Dụng

### 1. Update yt-dlp
- Đã update từ `2023.12.30` → `>=2024.1.1` (version mới nhất)

### 2. Thêm User-Agent Headers
- Thêm headers giống browser thật để tránh bot detection
- User-Agent: Chrome trên Windows

### 3. Sử Dụng Android Client
- Thay đổi từ web client sang android client
- Android client ít bị block hơn

### 4. Retry Logic
- Thêm retry với delay khi gặp lỗi bot detection
- Tự động retry 3 lần với delay tăng dần

### 5. Sleep Interval
- Thêm delay giữa các request để tránh rate limit

## Cách Deploy

1. **Push code mới:**
```bash
git add .
git commit -m "Fix YouTube bot detection"
git push origin main
```

2. **Chờ Render auto-deploy** (5-10 phút)

3. **Test lại:**
```
https://music-server-cdfv.onrender.com/get_audio_url?q=nhac
```

## Nếu Vẫn Bị Block

### Option 1: Đợi Một Chút
- YouTube có thể block tạm thời
- Đợi 10-30 phút rồi thử lại

### Option 2: Sử Dụng Cookies (Nâng Cao)
Nếu vẫn bị block, có thể cần cookies từ browser:
1. Đăng nhập YouTube trên browser
2. Export cookies (dùng extension như "Get cookies.txt LOCALLY")
3. Lưu vào file `cookies.txt` trong project
4. Thêm vào ydl_opts:
```python
'cookiefile': 'cookies.txt',
```

### Option 3: Sử Dụng YouTube API (Có Phí)
- Sử dụng YouTube Data API v3
- Cần API key (có giới hạn free)
- Tuân thủ ToS của YouTube

### Option 4: Proxy/VPN
- Thử deploy từ IP khác
- Hoặc dùng proxy service

## Kiểm Tra Logs

Sau khi deploy, kiểm tra logs trên Render:
- Nếu thấy `✅ Tìm thấy video` → Thành công!
- Nếu thấy `❌ LỖI` → Xem chi tiết lỗi

## Lưu Ý

- YouTube có thể thay đổi cách block bất cứ lúc nào
- Code đã được tối ưu để tránh bot detection
- Nếu vẫn lỗi, có thể cần đợi hoặc dùng cookies

