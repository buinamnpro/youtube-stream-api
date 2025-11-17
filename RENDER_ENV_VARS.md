# 🔧 Environment Variables Trên Render

## Cách Render Lưu Environment Variables

Render có thể lưu environment variables ở nhiều nơi:
1. **os.environ** - Thông thường (từ Render Dashboard)
2. **/etc/secrets/<filename>** - Render có thể lưu secrets ở đây
3. **File .env** - Trong app root (nếu có)

## Code Đã Hỗ Trợ

Code đã được cập nhật để đọc từ **cả 3 nơi**:
1. ✅ `os.environ.get('YOUTUBE_COOKIES')` - Thông thường
2. ✅ `/etc/secrets/YOUTUBE_COOKIES` - Render secrets
3. ✅ `.env` file trong app root

## Cách Thêm Environment Variable

### Cách 1: Qua Render Dashboard (Khuyến Nghị)

1. Vào **Render Dashboard**
2. Chọn service **music-server**
3. Vào **Settings** → **Environment**
4. Click **"Add Environment Variable"**
5. Thêm:
   - **Key:** `YOUTUBE_COOKIES`
   - **Value:** Paste toàn bộ nội dung cookies.txt
6. Click **"Save Changes"**
7. **Redeploy** service

### Cách 2: Qua Render CLI (Nếu Có)

```bash
render env:set YOUTUBE_COOKIES="<nội dung cookies>"
```

### Cách 3: Qua render.yaml (Không Khuyến Nghị)

Có thể thêm vào `render.yaml` nhưng **KHÔNG an toàn** vì sẽ commit lên GitHub.

## Kiểm Tra

Sau khi thêm và redeploy, logs sẽ hiển thị:

**Nếu tìm thấy:**
```
🍪 Tìm thấy YOUTUBE_COOKIES (length: 2500 chars)
🍪 Đã tạo cookies từ env variable: /app/cookies_env.txt
✅ File cookies đã tạo thành công (2500 bytes)
```

**Nếu không tìm thấy:**
```
⚠️ Không tìm thấy YOUTUBE_COOKIES env variable
   Đã thử: os.environ, /etc/secrets/YOUTUBE_COOKIES, .env file
   → Vào Render Dashboard → Settings → Environment
   → Thêm biến: Key=YOUTUBE_COOKIES, Value=<nội dung cookies.txt>
   → Save và Redeploy!
```

## Lưu Ý

- **Render thường dùng os.environ** - Đây là cách phổ biến nhất
- **/etc/secrets/** thường dùng cho secrets được quản lý bởi Render
- **.env file** chỉ dùng nếu bạn tự tạo (không khuyến nghị)

## Troubleshooting

### Nếu Vẫn Không Thấy:

1. **Kiểm tra tên biến:**
   - Phải đúng: `YOUTUBE_COOKIES` (chữ hoa)
   - Không có khoảng trắng

2. **Kiểm tra đã redeploy:**
   - Sau khi thêm env variable, PHẢI redeploy
   - Render có thể tự động redeploy, nhưng nên manual deploy để chắc chắn

3. **Kiểm tra giá trị:**
   - Phải copy TOÀN BỘ nội dung cookies.txt
   - Không thiếu dòng nào

4. **Xem logs chi tiết:**
   - Logs sẽ cho biết đã thử đọc từ đâu
   - Nếu không thấy ở đâu → Chưa được set đúng

