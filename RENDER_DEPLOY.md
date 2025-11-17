# 🚀 Hướng Dẫn Deploy Lên Render - Chi Tiết

## Bước 1: Chuẩn Bị Code

✅ Đảm bảo code đã được commit và push lên GitHub:
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

## Bước 2: Đăng Ký Render

1. Truy cập [render.com](https://render.com)
2. Click **"Get Started for Free"**
3. Đăng ký bằng GitHub (khuyến nghị) hoặc email

## Bước 3: Tạo Web Service

### ⚠️ Lưu Ý Quan Trọng về Blueprint

**Render Blueprint có thể cảnh báo về phí**, nhưng bạn vẫn có thể chọn **FREE TIER** khi deploy!

### Cách 1: Sử dụng render.yaml (Tự động)

1. Sau khi đăng nhập, click **"New +"** → **"Blueprint"**
2. Kết nối GitHub repository của bạn
3. Render sẽ tự động detect file `render.yaml` và cấu hình
4. **QUAN TRỌNG:** Khi preview, đảm bảo chọn **"Free" plan** cho service
5. Click **"Apply"** để deploy

**Nếu Render cảnh báo về phí:**
- Vẫn tiếp tục, nhưng khi tạo service, chọn **"Free"** plan
- Hoặc dùng **Cách 2** (Manual) để chắc chắn chọn free tier

### Cách 2: Tạo Manual (Khuyến nghị - Đảm bảo Free Tier) ✅

1. Click **"New +"** → **"Web Service"**
2. Kết nối GitHub repository của bạn
3. Chọn repository `music_server`
4. Cấu hình như sau:

   **Basic Settings:**
   - **Name:** `music-server` (hoặc tên bạn muốn)
   - **Region:** Chọn gần bạn nhất (Singapore, US, etc.)
   - **Branch:** `main` (hoặc branch bạn muốn deploy)
   - **Root Directory:** Để trống (hoặc `music_server` nếu code trong subfolder)

   **Build & Deploy:**
   - **Environment:** `Docker`
   - **Dockerfile Path:** `Dockerfile` (hoặc `music_server/Dockerfile` nếu trong subfolder)
   - **Docker Context:** `.` (hoặc `music_server` nếu trong subfolder)

   **Plan Settings (QUAN TRỌNG!):**
   - **Plan:** Chọn **"Free"** ✅ (KHÔNG chọn Starter hoặc các plan có phí)

   **Advanced Settings (Optional):**
   - **Auto-Deploy:** `Yes` (tự động deploy khi push code)
   - **Health Check Path:** `/get_audio_url?q=test` (để kiểm tra server)

5. **Đảm bảo đã chọn "Free" plan** → Click **"Create Web Service"**

## Bước 4: Chờ Deploy

- Render sẽ tự động build Docker image (có thể mất 5-10 phút lần đầu)
- Bạn có thể xem logs trong tab **"Logs"**
- Khi thấy `Application is live` → Deploy thành công! 🎉

## Bước 5: Lấy URL

1. Sau khi deploy xong, bạn sẽ thấy URL dạng:
   ```
   https://music-server-xxxx.onrender.com
   ```
2. Copy URL này để sử dụng

## Bước 6: Test API

Mở browser hoặc dùng curl để test:

```bash
# Test tìm kiếm và lấy URL
https://music-server-xxxx.onrender.com/get_audio_url?q=nhac

# Test stream trực tiếp
https://music-server-xxxx.onrender.com/stream?q=nhac
```

## Bước 7: Cập Nhật ESP32 Firmware

Thay đổi URL trong code ESP32:

**Trước:**
```cpp
String serverUrl = "http://localhost:5000";
```

**Sau:**
```cpp
String serverUrl = "https://music-server-xxxx.onrender.com";
```

## ⚙️ Cấu Hình Nâng Cao

### Tăng Timeout (Quan trọng cho stream audio)

1. Vào **Settings** của service trên Render
2. Tìm **"Health Check"** hoặc **"Advanced"**
3. Thêm biến môi trường:
   - Key: `GUNICORN_TIMEOUT`
   - Value: `300`

Hoặc chỉnh sửa trong Render dashboard → **Environment** → Add:
- `GUNICORN_TIMEOUT=300`

### Auto-Deploy

- Mặc định đã bật khi push code lên branch `main`
- Có thể tắt/bật trong **Settings** → **Auto-Deploy**

### Custom Domain (Tùy chọn)

1. Vào **Settings** → **Custom Domains**
2. Thêm domain của bạn
3. Cấu hình DNS theo hướng dẫn

## ⚠️ Lưu Ý Quan Trọng

### 1. Free Tier - HOÀN TOÀN MIỄN PHÍ ✅
- **Render có free tier và KHÔNG mất tiền!**
- Free tier: 750 giờ/tháng (đủ 24/7)
- **Bạn chỉ trả tiền nếu chủ động upgrade** ($7/tháng - tùy chọn)

### 2. Free Tier Sleep
- **Free tier sẽ sleep sau 15 phút không có request**
- Lần request đầu tiên sau khi sleep sẽ mất **~30 giây** để wake up
- **Giải pháp:** 
  - Dùng paid tier ($7/tháng) để không sleep (TÙY CHỌN)
  - Hoặc dùng service như [UptimeRobot](https://uptimerobot.com) để ping định kỳ (MIỄN PHÍ)

### 3. Timeout
- Free tier có timeout **90 giây**
- Với stream audio dài có thể cần tăng timeout
- Đã cấu hình `--timeout 300` trong Dockerfile

### 4. Build Time
- Lần đầu build có thể mất **5-10 phút** (cài FFmpeg, Python packages)
- Các lần sau nhanh hơn nhờ cache

### 5. Logs
- Xem logs trong tab **"Logs"** trên Render dashboard
- Logs giúp debug khi có lỗi

## 🔧 Troubleshooting

### Lỗi: "Build failed"
- Kiểm tra logs để xem lỗi cụ thể
- Đảm bảo Dockerfile đúng
- Kiểm tra requirements.txt

### Lỗi: "Application error"
- Kiểm tra logs
- Đảm bảo PORT được set đúng (Render tự động set)
- Kiểm tra app.py có lỗi syntax không

### Lỗi: "FFmpeg not found"
- Đảm bảo dùng Dockerfile (có cài FFmpeg)
- Không dùng buildpack Python (không có FFmpeg)

### Server sleep quá lâu
- Upgrade lên paid tier
- Hoặc dùng UptimeRobot để keep-alive

## 📊 Monitoring

- Xem metrics trong tab **"Metrics"**
- Monitor CPU, Memory, Request count
- Free tier có giới hạn, cần upgrade nếu vượt

## 🎉 Hoàn Thành!

Sau khi deploy thành công, server của bạn sẽ:
- ✅ Chạy online 24/7 (với free tier có sleep)
- ✅ Tự động deploy khi push code
- ✅ Có HTTPS tự động
- ✅ Có logs để debug

**URL của bạn:** `https://music-server-xxxx.onrender.com`

Chúc bạn deploy thành công! 🚀

