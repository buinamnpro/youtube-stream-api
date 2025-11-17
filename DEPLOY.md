# Hướng Dẫn Deploy Server Online

Server này có thể được deploy lên nhiều nền tảng cloud khác nhau. Dưới đây là hướng dẫn chi tiết:

## 🚀 Các Nền Tảng Đề Xuất

### 1. **Railway** (Dễ nhất - Khuyến nghị)
- ✅ Miễn phí $5/tháng
- ✅ Hỗ trợ Docker và Python trực tiếp
- ✅ Tự động deploy từ GitHub

**Cách deploy:**
1. Đăng ký tại [railway.app](https://railway.app)
2. Tạo project mới → "Deploy from GitHub repo"
3. Chọn repository của bạn
4. Railway tự động detect và deploy
5. Lấy URL từ dashboard

### 2. **Render** ⭐ **KHUYẾN NGHỊ CHO ỨNG DỤNG NÀY**
- ✅ **HOÀN TOÀN MIỄN PHÍ** - Free tier không mất tiền
- ✅ **Free tier:** 750 giờ/tháng (đủ cho 24/7 trong 1 tháng)
- ✅ **Dễ sử dụng:** Web UI đơn giản, không cần CLI
- ✅ **Auto-deploy từ GitHub:** Tự động deploy khi push code
- ✅ **Hỗ trợ Docker:** Có thể dùng Dockerfile (FFmpeg tự động cài)
- ⚠️ **Timeout:** 90 giây (đủ cho hầu hết trường hợp)
- ⚠️ **Sleep sau 15 phút không dùng:** Free tier sẽ sleep (có thể mất 30s để wake up)
- 💰 **Paid tier:** $7/tháng (chỉ cần nếu muốn không sleep + timeout dài hơn)

**Cách deploy:**
1. Đăng ký tại [render.com](https://render.com)
2. Tạo "Web Service" mới
3. Kết nối GitHub repository
4. Chọn:
   - Build Command: `pip install -r requirements.txt` (hoặc dùng Dockerfile)
   - Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 300`
5. Deploy!

### 3. **Fly.io**
- ✅ **Free tier:** 3 VMs miễn phí (256MB RAM mỗi VM)
- ✅ **Không sleep:** Luôn chạy 24/7
- ✅ **Tốc độ nhanh:** Edge deployment toàn cầu
- ✅ **Timeout dài:** Hỗ trợ request dài (phù hợp cho stream audio)
- ⚠️ **Cần CLI:** Phải cài đặt và sử dụng command line
- ⚠️ **Phức tạp hơn:** Cần cấu hình fly.toml

**Cách deploy:**
1. Cài đặt Fly CLI: `curl -L https://fly.io/install.sh | sh` (hoặc `iwr https://fly.io/install.ps1 -useb | iex` trên Windows)
2. Đăng nhập: `fly auth login`
3. Tạo app: `fly launch` (sẽ tự detect Dockerfile)
4. Deploy: `fly deploy`

## 🤔 **Render vs Fly.io - Nên Chọn Cái Nào?**

### **Chọn RENDER nếu:**
- ✅ Bạn muốn **dễ dàng nhất** - chỉ cần web UI, không cần CLI
- ✅ Bạn chấp nhận **sleep sau 15 phút** không dùng (wake up mất ~30s)
- ✅ Bạn muốn **auto-deploy từ GitHub** đơn giản
- ✅ Bạn không muốn cài đặt thêm công cụ

### **Chọn FLY.IO nếu:**
- ✅ Bạn cần server **luôn chạy 24/7** (không sleep)
- ✅ Bạn muốn **tốc độ nhanh** với edge deployment
- ✅ Bạn cần **timeout dài** cho stream audio
- ✅ Bạn không ngại dùng CLI

### **Khuyến nghị cho Music Server:**
**🎯 Chọn RENDER** vì:
1. Dễ deploy hơn (web UI)
2. Free tier đủ dùng (750h/tháng = 24/7)
3. Hỗ trợ Dockerfile tốt (FFmpeg tự động cài)
4. Auto-deploy từ GitHub tiện lợi

**⚠️ Lưu ý:** Nếu cần server luôn sẵn sàng (không sleep), chọn **Fly.io** hoặc upgrade Render lên paid tier.

### 4. **Heroku**
- ⚠️ Có phí (không còn free tier)
- ✅ Dễ sử dụng

**Cách deploy:**
1. Cài đặt Heroku CLI
2. Đăng nhập: `heroku login`
3. Tạo app: `heroku create your-app-name`
4. Deploy: `git push heroku main`

### 5. **PythonAnywhere**
- ✅ Miễn phí tier
- ✅ Dễ cho Python apps

**Cách deploy:**
1. Đăng ký tại [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload code qua Files tab
3. Tạo Web app trong Web tab
4. Cấu hình WSGI file trỏ đến app.py

## 📋 Yêu Cầu Trước Khi Deploy

1. **Đảm bảo code đã commit lên GitHub/GitLab**
2. **FFmpeg sẽ được cài tự động** (trong Dockerfile hoặc buildpack)

## 🔧 Cấu Hình Môi Trường

Nếu cần, bạn có thể set các biến môi trường:
- `PORT`: Port để chạy server (thường tự động set bởi platform)
- `HOST`: Host address (mặc định 0.0.0.0)
- `FFMPEG_PATH`: Đường dẫn FFmpeg (chỉ cần cho Windows local)

## 📝 Sử Dụng Sau Khi Deploy

Sau khi deploy, bạn sẽ có URL dạng: `https://your-app.railway.app`

**Test API:**
```
GET https://your-app.railway.app/get_audio_url?q=nhac
GET https://your-app.railway.app/stream?q=nhac
```

**Cập nhật firmware ESP32:**
Thay đổi URL server trong code ESP32 từ `http://localhost:5000` thành URL online của bạn.

## ⚠️ Lưu Ý

1. **Giới hạn tài nguyên**: Các nền tảng miễn phí có giới hạn CPU/RAM
2. **Timeout**: Một số platform có timeout request (đã set 300s trong gunicorn)
3. **Storage**: File tạm sẽ tự động xóa sau khi stream xong
4. **Rate limiting**: Có thể cần thêm rate limiting cho production

## 🐳 Deploy với Docker (Tùy chọn)

Nếu muốn chạy trên VPS hoặc server riêng:

```bash
docker build -t music-server .
docker run -p 5000:5000 music-server
```

## 📞 Hỗ Trợ

Nếu gặp vấn đề khi deploy, kiểm tra:
- Logs trên platform dashboard
- Đảm bảo FFmpeg được cài đặt
- Kiểm tra port configuration

