# ✅ Kiểm Tra Environment Variable Cookies

## Vấn Đề

Logs hiển thị:
```
⚠️ Không tìm thấy YOUTUBE_COOKIES env variable
```

→ Environment variable chưa được set hoặc chưa được nhận.

## Cách Kiểm Tra Và Sửa

### Bước 1: Kiểm Tra Trên Render Dashboard

1. **Vào Render Dashboard:** https://dashboard.render.com
2. **Chọn service:** `music-server`
3. **Vào Settings → Environment** (hoặc tab "Environment")
4. **Tìm biến:** `YOUTUBE_COOKIES`

**Nếu KHÔNG có:**
- Click **"Add Environment Variable"**
- **Key:** `YOUTUBE_COOKIES` (chính xác, không có khoảng trắng)
- **Value:** Paste toàn bộ nội dung cookies.txt
- Click **"Save Changes"**

**Nếu ĐÃ CÓ:**
- Click vào biến để xem/sửa
- Kiểm tra:
  - Tên có đúng `YOUTUBE_COOKIES` không? (chữ hoa)
  - Giá trị có đầy đủ không? (nên có > 2000 ký tự)
  - Có dòng đầu `# Netscape HTTP Cookie File` không?

### Bước 2: Redeploy (QUAN TRỌNG!)

**Sau khi thêm/sửa environment variable, PHẢI redeploy:**

1. Trong service `music-server`
2. Click tab **"Manual Deploy"**
3. Chọn **"Deploy latest commit"**
4. Đợi deploy xong (1-2 phút)

**HOẶC:**
- Render sẽ tự động redeploy khi bạn save env variable
- Nhưng nếu không, phải manual deploy

### Bước 3: Kiểm Tra Logs Sau Khi Deploy

Sau khi deploy xong, test lại API. Logs sẽ hiển thị:

**Nếu ĐÚNG:**
```
🍪 Tìm thấy YOUTUBE_COOKIES env variable (length: 2500 chars)
🍪 Đã tạo cookies từ env variable: /app/cookies_env.txt
✅ File cookies đã tạo thành công (2500 bytes)
✅ Format cookies có vẻ đúng
✅ Đã set cookiefile: /app/cookies_env.txt
```

**Nếu SAI:**
```
⚠️ Không tìm thấy YOUTUBE_COOKIES env variable
```

## Các Lỗi Thường Gặp

### 1. Tên Biến Sai

❌ **Sai:**
- `youtube_cookies` (chữ thường)
- `YOUTUBE_COOKIE` (thiếu S)
- `YOUTUBE_COOKIES ` (có khoảng trắng ở cuối)

✅ **Đúng:**
- `YOUTUBE_COOKIES` (chính xác)

### 2. Chưa Redeploy

❌ **Sai:** Thêm env variable nhưng không redeploy
✅ **Đúng:** Thêm env variable → Save → Redeploy

### 3. Copy Thiếu Nội Dung

❌ **Sai:** Chỉ copy một phần cookies
✅ **Đúng:** Copy TOÀN BỘ file từ dòng đầu đến dòng cuối

### 4. Format Sai

❌ **Sai:** Thêm/xóa spaces, tabs
✅ **Đúng:** Giữ nguyên format gốc

## Checklist

- [ ] Đã vào Render Dashboard
- [ ] Đã kiểm tra có biến `YOUTUBE_COOKIES` chưa
- [ ] Đã thêm/sửa biến với tên đúng `YOUTUBE_COOKIES`
- [ ] Đã copy TOÀN BỘ nội dung cookies.txt vào Value
- [ ] Đã save changes
- [ ] Đã redeploy service
- [ ] Đã kiểm tra logs có dòng `🍪 Tìm thấy YOUTUBE_COOKIES`

## Quick Fix

Nếu vẫn không thấy env variable:

1. **Xóa biến cũ** (nếu có)
2. **Thêm lại** với tên chính xác: `YOUTUBE_COOKIES`
3. **Copy lại** toàn bộ nội dung cookies.txt
4. **Save**
5. **Redeploy**

## Test

Sau khi fix, test lại:
```
https://music-server-cdfv.onrender.com/get_audio_url?q=nhac
```

Logs sẽ không còn lỗi bot detection nữa! ✅


