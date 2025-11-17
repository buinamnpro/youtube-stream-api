# ✅ Cách Deploy FREE TIER trên Render

## ⚠️ Nếu Render Báo "Mất Phí"

Render có thể cảnh báo khi dùng Blueprint (render.yaml), nhưng bạn **VẪN CÓ THỂ CHỌN FREE TIER**!

## 🎯 Giải Pháp: Tạo Manual (Đảm Bảo Free)

### Bước 1: Bỏ qua render.yaml, tạo service thủ công

1. Vào [render.com](https://render.com) → Đăng nhập
2. Click **"New +"** → **"Web Service"** (KHÔNG chọn Blueprint)
3. Kết nối GitHub → Chọn repo `music_server`

### Bước 2: Cấu hình (QUAN TRỌNG: Chọn Free Plan)

**Basic:**
- Name: `music-server`
- Region: Chọn gần bạn
- Branch: `main`

**Build & Deploy:**
- Environment: **Docker** ✅
- Dockerfile Path: `Dockerfile`
- Docker Context: `.`

**Plan (QUAN TRỌNG NHẤT!):**
- **Plan:** Chọn **"Free"** ✅
- **KHÔNG chọn** "Starter" hoặc các plan khác

**Advanced:**
- Auto-Deploy: `Yes`
- Health Check: `/get_audio_url?q=test`

### Bước 3: Tạo Service

Click **"Create Web Service"** → Chờ build (5-10 phút)

## ✅ Xác Nhận Free Tier

Sau khi tạo, kiểm tra:
1. Vào **Settings** của service
2. Xem **Plan** → Phải hiển thị **"Free"**
3. Nếu thấy "Starter" hoặc plan có phí → Click **"Change Plan"** → Chọn **"Free"**

## 💰 Kiểm Tra Billing

1. Vào **Account Settings** → **Billing**
2. Phải thấy **$0.00** hoặc **"No charges"**
3. Nếu có phí → Kiểm tra lại plan của service

## 🎉 Kết Quả

- ✅ Service chạy trên **Free Tier**
- ✅ **Không mất phí**
- ✅ Có thể dùng mãi mãi (trong giới hạn 750h/tháng)

## ⚠️ Lưu Ý

- **Render KHÔNG tự động charge** nếu bạn chọn Free plan
- **Có thể downgrade** bất cứ lúc nào từ paid → free
- **Free tier có sleep** sau 15 phút (bình thường, không ảnh hưởng nhiều)

