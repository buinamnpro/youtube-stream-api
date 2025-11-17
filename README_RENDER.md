# 🎵 Music Server - Quick Start với Render

## ⚡ Deploy Nhanh (3 Bước)

### 1. Push code lên GitHub
```bash
git add .
git commit -m "Ready for Render"
git push origin main
```

### 2. Deploy trên Render
1. Vào [render.com](https://render.com) → Đăng ký/Đăng nhập
2. Click **"New +"** → **"Blueprint"**
3. Kết nối GitHub repo → Chọn repo `music_server`
4. Click **"Apply"** → Chờ 5-10 phút

### 3. Lấy URL và dùng
- URL sẽ có dạng: `https://music-server-xxxx.onrender.com`
- Test: `https://music-server-xxxx.onrender.com/get_audio_url?q=nhac`

## 📝 Chi Tiết

Xem file **RENDER_DEPLOY.md** để biết hướng dẫn chi tiết từng bước.

## ⚠️ Lưu Ý

- Free tier sẽ **sleep sau 15 phút** không dùng
- Lần đầu wake up mất **~30 giây**
- Nếu cần 24/7 không sleep → Upgrade lên paid tier ($7/tháng)

## 🔗 Links

- [Render Dashboard](https://dashboard.render.com)
- [Documentation](https://render.com/docs)

