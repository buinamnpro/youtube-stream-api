# ⚡ Quick Fix - YouTube Bot Detection

## Vấn Đề Hiện Tại

Từ logs, tôi thấy:
1. ✅ yt-dlp **ĐÃ TÌM THẤY** video (fUu2KrYRqJg)
2. ❌ Nhưng khi lấy **metadata** thì bị YouTube block
3. YouTube yêu cầu: "Đăng nhập để xác nhận bạn không phải là bot"

## Giải Pháp Đã Áp Dụng

### 1. ✅ Dùng `extract_flat=True`
- Chỉ lấy **URL video**, không cần metadata
- Tránh được bước lấy metadata (dễ bị block)
- Nhanh hơn và ít bị block hơn

### 2. ✅ Chỉ Dùng Android Client
- Bỏ web client (dễ bị block)
- Chỉ dùng Android client
- Android client ít bị block hơn

### 3. ✅ Xử Lý Lỗi Tốt Hơn
- Nếu không lấy được metadata → dùng giá trị mặc định
- Vẫn có thể stream được dù không có title/artist

## Cách Deploy

```bash
git add .
git commit -m "Fix: Use extract_flat to avoid metadata bot detection"
git push origin main
```

## Kết Quả Mong Đợi

Sau khi deploy:
- ✅ Tìm kiếm sẽ thành công (đã tìm thấy video)
- ✅ Có thể stream được ngay
- ⚠️ Title/Artist có thể là giá trị mặc định nếu bị block metadata

## Test

Sau khi deploy xong, test:
```
https://music-server-cdfv.onrender.com/get_audio_url?q=nhac
```

Nếu thành công, bạn sẽ thấy:
```json
{
  "status": "success",
  "title": "YouTube Video fUu2KrYRqJg" hoặc tên thật,
  "audio_url": "https://...",
  ...
}
```

## Nếu Vẫn Lỗi

Nếu vẫn bị block khi tìm kiếm (không phải metadata):
- Đợi 10-30 phút rồi thử lại
- Hoặc dùng URL YouTube trực tiếp: `?url=https://www.youtube.com/watch?v=VIDEO_ID`

