# 🍪 Cách Thêm Cookies Lên Render

## Vấn Đề

File `cookies.txt` có ở local nhưng **không có trên Render server**, nên bị block khi download.

## Giải Pháp (3 Cách)

### Cách 1: Dùng Environment Variable (Khuyến Nghị - An Toàn) ✅

**Ưu điểm:**
- ✅ Không cần commit cookies lên GitHub
- ✅ An toàn, chỉ có trên Render
- ✅ Dễ quản lý

**Cách làm:**

1. **Đọc nội dung file cookies.txt:**
   ```bash
   # Trên Windows PowerShell
   Get-Content cookies.txt | Out-String
   ```

2. **Vào Render Dashboard:**
   - Chọn service `music-server`
   - Vào **Settings** → **Environment**
   - Click **"Add Environment Variable"**

3. **Thêm biến:**
   - **Key:** `YOUTUBE_COOKIES`
   - **Value:** Paste toàn bộ nội dung file cookies.txt
   - Click **"Save Changes"**

4. **Redeploy service** (Render sẽ tự động redeploy)

### Cách 2: Upload Qua Render Shell

1. **Vào Render Dashboard:**
   - Chọn service `music-server`
   - Click tab **"Shell"**

2. **Upload file:**
   ```bash
   # Tạo file cookies.txt
   nano cookies.txt
   # Paste nội dung cookies.txt vào
   # Save: Ctrl+X, Y, Enter
   ```

3. **Hoặc dùng SCP/SFTP** (nếu có quyền)

### Cách 3: Copy Vào Dockerfile (Không Khuyến Nghị)

⚠️ **CẢNH BÁO:** Sẽ commit cookies lên GitHub nếu không cẩn thận!

Nếu muốn dùng cách này:
1. Tạm thời bỏ cookies.txt khỏi .gitignore
2. Commit cookies.txt
3. Push lên GitHub
4. Render sẽ build với cookies
5. **Sau đó xóa cookies.txt khỏi git ngay!**

## Cách Kiểm Tra

Sau khi thêm cookies, logs sẽ hiển thị:
```
🍪 Sử dụng cookies từ file: /app/cookies.txt
```
hoặc
```
🍪 Sử dụng cookies từ environment variable
```

Thay vì:
```
⚠️ Không tìm thấy cookies.txt, có thể bị block
```

## Khuyến Nghị

**→ Dùng Cách 1 (Environment Variable)** vì:
- ✅ An toàn nhất
- ✅ Không cần commit cookies
- ✅ Dễ quản lý và update

## Lưu Ý

- Cookies có thể hết hạn sau một thời gian
- Nếu bị block lại, cần export cookies mới
- Update environment variable trên Render

