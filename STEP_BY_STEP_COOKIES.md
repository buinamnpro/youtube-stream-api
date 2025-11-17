# 🍪 Hướng Dẫn Chi Tiết: Thêm Cookies Lên Render

## ⚠️ Vấn Đề Hiện Tại

Logs hiển thị:
```
⚠️ Không tìm thấy cookies.txt, có thể bị block
ERROR: Sign in to confirm you're not a bot
```

→ **Chưa có cookies trên Render server!**

## Giải Pháp: Thêm Environment Variable

### Bước 1: Mở File cookies.txt

Mở file `cookies.txt` trong thư mục `music_server/`

### Bước 2: Copy Toàn Bộ Nội Dung

**Copy TẤT CẢ** từ dòng đầu đến dòng cuối, bao gồm:
- Dòng comment `# Netscape HTTP Cookie File`
- Tất cả các dòng cookies

**Ví dụ format:**
```
# Netscape HTTP Cookie File
# https://curl.haxx.se/rfc/cookie_spec.html
# This is a generated file! Do not edit.

.youtube.com	TRUE	/	TRUE	1797966546	PREF	f6=40000000&tz=Asia.Saigon&f5=30000&f7=100
.youtube.com	TRUE	/	FALSE	1797966523	HSID	AYAeFGZ88nUV0OhT_
...
```

### Bước 3: Vào Render Dashboard

1. Mở: https://dashboard.render.com
2. Đăng nhập (nếu chưa)
3. Tìm và click vào service **music-server**

### Bước 4: Thêm Environment Variable

1. Trong service `music-server`, click tab **"Environment"** (hoặc vào **Settings** → **Environment**)
2. Scroll xuống phần **"Environment Variables"**
3. Click nút **"Add Environment Variable"** hoặc **"+ Add"**
4. Điền:
   - **Key:** `YOUTUBE_COOKIES`
   - **Value:** Paste toàn bộ nội dung file cookies.txt (đã copy ở bước 2)
5. Click **"Save Changes"** hoặc **"Add"**

### Bước 5: Redeploy Service

Sau khi save, Render sẽ tự động redeploy. Hoặc:

1. Click tab **"Manual Deploy"**
2. Chọn **"Deploy latest commit"**
3. Đợi deploy xong (1-2 phút)

### Bước 6: Kiểm Tra Logs

Sau khi deploy xong, test lại API. Logs sẽ hiển thị:
```
🍪 Sử dụng cookies từ environment variable
```

Thay vì:
```
⚠️ Không tìm thấy cookies.txt, có thể bị block
```

## Lưu Ý Quan Trọng

### ✅ Phải Copy Đúng Format

- Phải copy **TOÀN BỘ** file, không bỏ sót dòng nào
- Giữ nguyên format (tabs, spaces)
- Không thêm/xóa ký tự

### ⚠️ Cookies Có Thể Hết Hạn

- Cookies YouTube thường hết hạn sau 1-3 tháng
- Nếu bị block lại, cần export cookies mới
- Update environment variable trên Render

### 🔒 Bảo Mật

- Environment variable chỉ có trên Render
- Không ai có thể thấy cookies
- An toàn hơn commit file lên GitHub

## Troubleshooting

### Nếu Vẫn Bị Block:

1. **Kiểm tra cookies có hết hạn không:**
   - Export cookies mới từ browser
   - Update environment variable

2. **Kiểm tra format:**
   - Đảm bảo copy đúng toàn bộ file
   - Không có ký tự lạ

3. **Kiểm tra logs:**
   - Xem có dòng `🍪 Sử dụng cookies từ environment variable` không
   - Nếu không có → Environment variable chưa được set đúng

4. **Redeploy lại:**
   - Có thể cần redeploy để env variable có hiệu lực

## Quick Checklist

- [ ] Đã mở file cookies.txt
- [ ] Đã copy toàn bộ nội dung
- [ ] Đã vào Render Dashboard
- [ ] Đã thêm environment variable `YOUTUBE_COOKIES`
- [ ] Đã paste toàn bộ nội dung cookies vào Value
- [ ] Đã save changes
- [ ] Đã redeploy service
- [ ] Đã kiểm tra logs có dòng `🍪 Sử dụng cookies`

## Sau Khi Thêm

Sau khi thêm cookies và redeploy, test lại:
```
https://music-server-cdfv.onrender.com/get_audio_url?q=nhac
```

Logs sẽ không còn lỗi bot detection nữa! ✅

