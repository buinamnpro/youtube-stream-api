# ✅ Checklist Deploy Render

## Trước Khi Deploy

- [ ] Code đã được commit và push lên GitHub
- [ ] Đã kiểm tra các file cần thiết:
  - [x] `Dockerfile` ✓
  - [x] `render.yaml` ✓
  - [x] `requirements.txt` ✓
  - [x] `app.py` ✓

## Bước Deploy

- [ ] Đăng ký/Đăng nhập tại [render.com](https://render.com)
- [ ] Click **"New +"** → **"Blueprint"**
- [ ] Kết nối GitHub account
- [ ] Chọn repository `music_server`
- [ ] Click **"Apply"** để deploy
- [ ] Chờ build hoàn tất (5-10 phút)

## Sau Khi Deploy

- [ ] Copy URL từ Render dashboard
- [ ] Test API: `https://your-url.onrender.com/get_audio_url?q=test`
- [ ] Cập nhật URL trong ESP32 firmware
- [ ] Test với ESP32

## Lưu Ý

- ⚠️ Free tier sẽ sleep sau 15 phút không dùng
- ⚠️ Lần đầu wake up mất ~30 giây
- ✅ Auto-deploy đã bật (tự động deploy khi push code)

---

**URL của bạn:** `https://____________________.onrender.com`

