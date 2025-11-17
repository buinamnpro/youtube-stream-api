# 🔍 Debug: Kiểm Tra Cookies Trên Render

## Vấn Đề

Bạn đã thêm environment variable `YOUTUBE_COOKIES` nhưng vẫn bị block.

## Cách Kiểm Tra

### Bước 1: Kiểm Tra Logs

Sau khi deploy code mới, xem logs trên Render. Bạn sẽ thấy một trong các dòng:

**Nếu env variable đã được set:**
```
🍪 Tìm thấy YOUTUBE_COOKIES env variable (length: xxxx chars)
🍪 Đã tạo cookies từ env variable: /app/cookies_env.txt
✅ File cookies đã tạo thành công (xxxx bytes)
```

**Nếu env variable chưa được set:**
```
⚠️ Không tìm thấy YOUTUBE_COOKIES env variable
⚠️ Không tìm thấy cookies.txt, có thể bị block
```

### Bước 2: Kiểm Tra Environment Variable Trên Render

1. Vào **Render Dashboard**
2. Chọn service **music-server**
3. Vào **Settings** → **Environment**
4. Kiểm tra xem có biến `YOUTUBE_COOKIES` không:
   - Nếu có → Xem giá trị có đúng không
   - Nếu không có → Cần thêm lại

### Bước 3: Kiểm Tra Format Cookies

Environment variable phải chứa **TOÀN BỘ** nội dung file cookies.txt, bao gồm:
- Dòng comment đầu tiên: `# Netscape HTTP Cookie File`
- Tất cả các dòng cookies
- Giữ nguyên format (tabs giữa các cột)

**Ví dụ đúng:**
```
# Netscape HTTP Cookie File
# https://curl.haxx.se/rfc/cookie_spec.html
# This is a generated file! Do not edit.

.youtube.com	TRUE	/	TRUE	1797966546	PREF	f6=40000000&tz=Asia.Saigon&f5=30000&f7=100
...
```

### Bước 4: Redeploy Sau Khi Thêm Env Variable

**QUAN TRỌNG:** Sau khi thêm/sửa environment variable, **PHẢI redeploy**!

1. Click **"Manual Deploy"**
2. Chọn **"Deploy latest commit"**
3. Đợi deploy xong

## Các Vấn Đề Thường Gặp

### 1. Chưa Redeploy

❌ **Sai:** Thêm env variable nhưng không redeploy
✅ **Đúng:** Thêm env variable → Save → Redeploy

### 2. Copy Thiếu Nội Dung

❌ **Sai:** Chỉ copy một phần cookies
✅ **Đúng:** Copy TOÀN BỘ file từ dòng đầu đến dòng cuối

### 3. Format Sai

❌ **Sai:** Thêm/xóa spaces, tabs
✅ **Đúng:** Giữ nguyên format gốc

### 4. Cookies Hết Hạn

Nếu cookies đã hết hạn:
- Export cookies mới từ browser
- Update environment variable trên Render
- Redeploy

## Checklist Debug

- [ ] Đã thêm environment variable `YOUTUBE_COOKIES` trên Render
- [ ] Đã copy TOÀN BỘ nội dung cookies.txt (không thiếu dòng nào)
- [ ] Đã save changes trên Render
- [ ] Đã redeploy service sau khi thêm env variable
- [ ] Đã kiểm tra logs có dòng `🍪 Tìm thấy YOUTUBE_COOKIES`
- [ ] Đã kiểm tra logs có dòng `✅ File cookies đã tạo thành công`

## Sau Khi Fix

Nếu mọi thứ đúng, logs sẽ hiển thị:
```
🍪 Tìm thấy YOUTUBE_COOKIES env variable (length: 2500 chars)
🍪 Đã tạo cookies từ env variable: /app/cookies_env.txt
✅ File cookies đã tạo thành công (2500 bytes)
📥 Đang tải và chuyển đổi sang MP3...
✅ Tải và chuyển đổi thành công!
```

Và sẽ **KHÔNG còn** lỗi:
```
ERROR: Sign in to confirm you're not a bot
```

