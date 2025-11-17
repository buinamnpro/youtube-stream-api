# ⚠️ Cookies Đã Hết Hạn Hoặc Bị Rotate

## Vấn Đề

Logs hiển thị:
```
WARNING: The provided YouTube account cookies are no longer valid. 
They have likely been rotated in the browser as a security measure.
```

→ **Cookies đã hết hạn hoặc bị YouTube rotate!**

## Giải Pháp: Export Cookies Mới

### Bước 1: Export Cookies Mới

1. **Mở browser** (Chrome/Edge/Firefox)
2. **Đăng nhập YouTube** (quan trọng!)
3. **Vào bất kỳ trang YouTube nào**
4. **Dùng extension** "Get cookies.txt LOCALLY":
   - Click extension icon
   - Click "Export" hoặc "Download"
   - Save file thành `cookies.txt`

### Bước 2: Update Environment Variable Trên Render

1. **Mở file cookies.txt mới** vừa export
2. **Copy TOÀN BỘ** nội dung (Ctrl+A, Ctrl+C)
3. **Vào Render Dashboard:**
   - Chọn service `music-server`
   - Settings → Environment
   - Tìm biến `YOUTUBE_COOKIES`
   - Click để edit
   - Paste nội dung cookies mới
   - Save Changes
4. **Redeploy** service

### Bước 3: Kiểm Tra

Sau khi redeploy, test lại API. Logs sẽ không còn cảnh báo cookies hết hạn.

## Lưu Ý

### Cookies Thường Hết Hạn Sau:

- **1-3 tháng** - Tùy vào YouTube policy
- **Khi đổi password** - YouTube sẽ rotate cookies
- **Khi có hoạt động bất thường** - YouTube có thể rotate cookies

### Cách Phát Hiện Cookies Hết Hạn:

- Logs hiển thị: "cookies are no longer valid"
- API bị block: "Sign in to confirm you're not a bot"
- Download thất bại

### Cách Tránh Cookies Hết Hạn:

- **Export cookies thường xuyên** (mỗi tháng 1 lần)
- **Không đổi password** YouTube thường xuyên
- **Dùng account ổn định** (ít bị flag)

## Code Đã Được Sửa

Code đã được cập nhật để:
- ✅ Dùng **web client** khi có cookies (android không hỗ trợ cookies)
- ✅ Tự động detect cookies từ `/etc/secrets/YOUTUBE_COOKIES`
- ✅ Logging chi tiết để debug

## Sau Khi Update Cookies

Logs sẽ hiển thị:
```
🍪 Đọc cookies từ /etc/secrets/YOUTUBE_COOKIES
🍪 Tìm thấy YOUTUBE_COOKIES (length: 2562 chars)
✅ Đã set cookiefile: /app/cookies_env.txt
✅ Đã set player_client=web (cookies yêu cầu web client)
📥 Đang tải và chuyển đổi sang MP3...
✅ Tải và chuyển đổi thành công!
```

**KHÔNG còn** cảnh báo:
```
WARNING: cookies are no longer valid
```

