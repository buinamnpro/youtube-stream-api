# ⚡ Quick: Thêm Cookies Lên Render

## Vấn Đề

Logs hiển thị:
```
⚠️ Không tìm thấy cookies.txt, có thể bị block
```

→ Cookies chỉ có ở local, chưa có trên Render.

## Giải Pháp Nhanh: Dùng Environment Variable ✅

### Bước 1: Copy Nội Dung Cookies

Mở file `cookies.txt` và copy **TOÀN BỘ** nội dung.

### Bước 2: Thêm Vào Render

1. Vào **Render Dashboard**
2. Chọn service **music-server**
3. Vào **Settings** → **Environment**
4. Click **"Add Environment Variable"**
5. Thêm:
   - **Key:** `YOUTUBE_COOKIES`
   - **Value:** Paste toàn bộ nội dung cookies.txt
6. Click **"Save Changes"**

### Bước 3: Redeploy

Render sẽ tự động redeploy. Hoặc click **"Manual Deploy"** → **"Deploy latest commit"**

## Kiểm Tra

Sau khi deploy, logs sẽ hiển thị:
```
🍪 Sử dụng cookies từ environment variable
```

Thay vì:
```
⚠️ Không tìm thấy cookies.txt, có thể bị block
```

## Lưu Ý

- Cookies có thể hết hạn sau vài tháng
- Nếu bị block lại, export cookies mới và update env variable
- Xem `ADD_COOKIES_TO_RENDER.md` để biết các cách khác

