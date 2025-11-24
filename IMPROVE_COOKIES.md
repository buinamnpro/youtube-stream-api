# 🔧 Cải Thiện Sử Dụng Cookies

## Các Cải Tiến Đã Thực Hiện

### 1. Kiểm Tra Format Cookies

Code sẽ tự động kiểm tra format cookies file:
- Kiểm tra dòng đầu có chứa "Netscape" không
- Kiểm tra có chứa "youtube.com" không
- Cảnh báo nếu format không đúng

### 2. Cải Thiện Error Handling

- Logging chi tiết hơn khi tạo cookies từ env variable
- Kiểm tra file đã tạo thành công chưa
- Hiển thị file size để debug

### 3. Thêm Options Bypass Bot Detection

Khi có cookies, code sẽ:
- Dùng cả `android` và `web` player client
- Thêm `sleep_interval` để tránh rate limit
- Cải thiện extractor args

## Kiểm Tra Cookies Có Hoạt Động

Sau khi deploy, logs sẽ hiển thị:

```
🍪 Tìm thấy YOUTUBE_COOKIES env variable (length: 2500 chars)
🍪 Đã tạo cookies từ env variable: /app/cookies_env.txt
✅ File cookies đã tạo thành công (2500 bytes)
✅ Format cookies có vẻ đúng
✅ Đã set cookiefile: /app/cookies_env.txt
```

## Vấn Đề Vẫn Có Thể Gặp

### 1. Cookies Hết Hạn

Nếu cookies đã hết hạn:
- Export cookies mới từ browser
- Update environment variable trên Render
- Redeploy

### 2. Format Cookies Sai

Đảm bảo cookies file có format Netscape:
```
# Netscape HTTP Cookie File
.youtube.com	TRUE	/	TRUE	1797966546	PREF	value
```

### 3. Thiếu Cookies Quan Trọng

Cookies phải có các cookies quan trọng:
- `__Secure-1PSID`
- `__Secure-1PSIDTS`
- `LOGIN_INFO`
- `VISITOR_INFO1_LIVE`

## Cách Export Cookies Đúng

1. **Đăng nhập YouTube** trên browser
2. **Dùng extension** "Get cookies.txt LOCALLY"
3. **Export cookies** từ YouTube
4. **Copy toàn bộ** nội dung vào environment variable
5. **Redeploy** service

## Debug

Nếu vẫn bị block, kiểm tra logs:
- Có dòng `✅ Đã set cookiefile` không?
- File size có hợp lý không? (thường > 2000 bytes)
- Format có đúng không?

Nếu tất cả đều đúng nhưng vẫn block → Cookies có thể đã hết hạn, cần export mới.


