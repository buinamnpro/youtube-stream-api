# 🐛 Hướng Dẫn Debug - Tìm Kiếm YouTube

## Vấn Đề: "Không tìm thấy video"

### 1. Kiểm Tra Logs Trên Render

1. Vào Render Dashboard → Chọn service `music-server`
2. Click tab **"Logs"**
3. Xem các dòng log có emoji:
   - 🔍 Đang tìm kiếm
   - 📊 Kết quả tìm kiếm
   - ✅ Tìm thấy video
   - ❌ LỖI TÌM KIẾM

### 2. Test Với Từ Khóa Khác

Thử các từ khóa khác để xác định vấn đề:

**Test 1: Từ khóa tiếng Anh**
```
https://music-server-cdfv.onrender.com/get_audio_url?q=hello
```

**Test 2: Từ khóa tiếng Việt đơn giản**
```
https://music-server-cdfv.onrender.com/get_audio_url?q=nhac
```

**Test 3: Từ khóa có dấu (URL encoded)**
```
https://music-server-cdfv.onrender.com/get_audio_url?q=h%C3%A3y+trao+cho+anh
```

**Test 4: Dùng URL YouTube trực tiếp**
```
https://music-server-cdfv.onrender.com/get_audio_url?url=https://www.youtube.com/watch?v=VIDEO_ID
```

### 3. Các Nguyên Nhân Có Thể

#### A. yt-dlp không tìm thấy video
- **Nguyên nhân:** Từ khóa quá cụ thể hoặc không phổ biến
- **Giải pháp:** Thử từ khóa khác, hoặc dùng URL YouTube trực tiếp

#### B. Lỗi kết nối với YouTube
- **Nguyên nhân:** YouTube block hoặc rate limit
- **Giải pháp:** Đợi một chút rồi thử lại

#### C. Lỗi encoding
- **Nguyên nhân:** Ký tự đặc biệt không được encode đúng
- **Giải pháp:** Đã fix trong code mới (decode URL)

#### D. yt-dlp cần update
- **Nguyên nhân:** Version cũ không hỗ trợ tốt
- **Giải pháp:** Update requirements.txt

### 4. Cách Fix Nhanh

#### Option 1: Dùng URL YouTube Trực Tiếp
Thay vì tìm kiếm, dùng URL trực tiếp:
```
https://music-server-cdfv.onrender.com/get_audio_url?url=https://www.youtube.com/watch?v=VIDEO_ID
```

#### Option 2: Test Local Trước
Chạy server local để test:
```bash
python app.py
```
Sau đó test: `http://localhost:5000/get_audio_url?q=nhac`

#### Option 3: Kiểm Tra yt-dlp Version
Có thể cần update yt-dlp:
```bash
pip install --upgrade yt-dlp
```

### 5. Kiểm Tra Logs Chi Tiết

Sau khi deploy code mới, logs sẽ hiển thị:
```
🔍 Đang tìm kiếm: 'hãy trao cho anh'
📊 Kết quả tìm kiếm: {...}
✅ Tìm thấy video: https://...
```

Nếu thấy lỗi, sẽ có:
```
❌ LỖI TÌM KIẾM YOUTUBE: [chi tiết lỗi]
```

### 6. Test Sau Khi Deploy Code Mới

1. Push code mới lên GitHub
2. Render sẽ auto-deploy
3. Chờ deploy xong (5-10 phút)
4. Test lại với cùng URL

## 📝 Ghi Chú

- Code mới đã cải thiện:
  - ✅ Decode URL encoding đúng cách
  - ✅ Logging chi tiết hơn
  - ✅ Error handling tốt hơn
  - ✅ Xử lý entries None

- Nếu vẫn lỗi sau khi deploy code mới:
  - Kiểm tra logs trên Render
  - Thử với từ khóa khác
  - Thử với URL YouTube trực tiếp

