# 🎵 Hướng Dẫn Stream MP3

## Tình Trạng Hiện Tại

✅ **API đã trả về thành công:**
```json
{
  "status": "success",
  "audio_url": "https://music-server-cdfv.onrender.com/stream_mp3/8dde8e44ce594993aa65bfae46dbb8aa",
  "title": "Nơi Này Có Anh...",
  "artist": "Sky Lofi Chill"
}
```

## Cách Stream MP3

### Bước 1: Truy Cập `audio_url`

Mở browser hoặc dùng curl:
```
https://music-server-cdfv.onrender.com/stream_mp3/8dde8e44ce594993aa65bfae46dbb8aa
```

### Bước 2: Chờ Download & Convert

Khi truy cập `audio_url`, server sẽ:
1. 📥 Download video từ YouTube
2. 🔄 Convert sang MP3 (có thể mất 1-3 phút)
3. 📤 Stream MP3 về client

### Bước 3: Xem Logs

Trong Render Dashboard → Logs, bạn sẽ thấy:
```
🎵 Nhận yêu cầu stream MP3 cho token: 8dde8e44ce594993aa65bfae46dbb8aa
🎵 Stream video: Nơi Này Có Anh...
🎵 YouTube URL: https://www.youtube.com/watch?v=HK_ozvD4GcQ
🔄 Bắt đầu chuyển đổi MP3...
📥 Bắt đầu tải video: ...
📥 Đang tải và chuyển đổi sang MP3...
✅ Tải và chuyển đổi thành công!
✅ Đã tạo MP3, bắt đầu stream: ...
📊 File size: xxxxx bytes
📤 Đã gửi: xxxxx/xxxxx bytes (xx%)
✅ Hoàn thành stream MP3
```

## Vấn Đề Có Thể Gặp

### 1. Timeout (90 giây)
- **Render free tier có timeout 90 giây**
- Video dài (>3 phút) có thể không kịp download/convert
- **Giải pháp:** Upgrade lên paid tier hoặc dùng video ngắn hơn

### 2. YouTube Block
- YouTube có thể block khi download
- **Giải pháp:** Đợi một chút rồi thử lại

### 3. FFmpeg Lỗi
- FFmpeg có thể không convert được
- **Giải pháp:** Kiểm tra logs để xem lỗi cụ thể

### 4. Không Thấy Response
- Browser có thể đang chờ (đang download/convert)
- **Giải pháp:** Đợi 1-3 phút, hoặc xem logs

## Test Nhanh

### Test với curl:
```bash
curl -v "https://music-server-cdfv.onrender.com/stream_mp3/8dde8e44ce594993aa65bfae46dbb8aa" -o test.mp3
```

### Test với browser:
1. Mở `audio_url` trong browser
2. Browser sẽ tự động download hoặc play MP3
3. Xem logs trên Render để biết tiến độ

## Kiểm Tra Logs

Nếu không thấy stream, kiểm tra logs trên Render:
1. Vào Render Dashboard
2. Chọn service `music-server`
3. Click tab **"Logs"**
4. Tìm các dòng:
   - `🎵 Nhận yêu cầu stream MP3` - Đã nhận request
   - `🔄 Bắt đầu chuyển đổi MP3` - Đang convert
   - `✅ Tải và chuyển đổi thành công` - Thành công
   - `❌ LỖI` - Có lỗi

## Lưu Ý

- **Lần đầu stream có thể mất 1-3 phút** (download + convert)
- **Video dài (>5 phút) có thể timeout** trên free tier
- **Nếu timeout, cần upgrade** lên paid tier ($7/tháng)

## Kết Luận

API đã hoạt động đúng! Bây giờ bạn cần:
1. ✅ Truy cập `audio_url` để stream MP3
2. ⏳ Đợi 1-3 phút để download/convert
3. 📊 Xem logs trên Render để biết tiến độ

