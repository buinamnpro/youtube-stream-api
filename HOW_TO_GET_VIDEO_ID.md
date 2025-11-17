# 🔍 Làm Sao Để Biết Video ID?

## Cách yt-dlp Trả Về Video ID

### Khi Dùng `extract_flat=True`

Khi bạn tìm kiếm với `extract_flat=True`, yt-dlp trả về cấu trúc như sau:

```python
info = {
    'entries': [
        {
            'id': 'fUu2KrYRqJg',  # ← Video ID ở đây!
            'url': 'https://www.youtube.com/watch?v=fUu2KrYRqJg',
            'title': 'Hãy Trao Cho Anh',  # Có thể có hoặc không
            # ... các thông tin khác
        }
    ]
}
```

### Cách Code Lấy ID

Trong code hiện tại (dòng 64-79):

```python
if info and 'entries' in info:
    entries = [e for e in info['entries'] if e]  # Loại bỏ None
    if len(entries) > 0:
        entry = entries[0]  # Lấy video đầu tiên
        
        # Cách 1: Lấy ID trực tiếp
        video_id = entry.get('id')  # ← Lấy ID từ đây!
        if video_id:
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            return video_url
        
        # Cách 2: Lấy URL có sẵn
        video_url = entry.get('webpage_url') or entry.get('url')
        if video_url:
            return video_url
```

## Ví Dụ Cụ Thể

### Tìm Kiếm: "nhac"

**Bước 1: yt-dlp tìm kiếm**
```python
query = "nhac"
info = ydl.extract_info("ytsearch1:nhac", download=False)
```

**Bước 2: yt-dlp trả về**
```python
info = {
    'entries': [
        {
            'id': 'fUu2KrYRqJg',  # ← ID này!
            'url': 'https://www.youtube.com/watch?v=fUu2KrYRqJg',
            'title': 'Hãy Trao Cho Anh',
        }
    ]
}
```

**Bước 3: Code lấy ID**
```python
entry = info['entries'][0]
video_id = entry.get('id')  # = 'fUu2KrYRqJg'
video_url = f"https://www.youtube.com/watch?v={video_id}"
# = 'https://www.youtube.com/watch?v=fUu2KrYRqJg'
```

## Các Cách Lấy Video ID

### Cách 1: Từ Kết Quả Tìm Kiếm (Hiện Tại)
```python
video_id = entry.get('id')  # 'fUu2KrYRqJg'
```

### Cách 2: Từ URL YouTube
```python
url = "https://www.youtube.com/watch?v=fUu2KrYRqJg"
video_id = url.split('v=')[1].split('&')[0]  # 'fUu2KrYRqJg'
```

### Cách 3: Dùng Regex (Trong Code)
```python
import re
url = "https://www.youtube.com/watch?v=fUu2KrYRqJg"
match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11})', url)
video_id = match.group(1)  # 'fUu2KrYRqJg'
```

## Debug: Xem ID Như Thế Nào?

### Trong Logs Render

Khi code chạy, bạn sẽ thấy trong logs:

```
🔍 Đang tìm kiếm (lần 1/3): 'nhac'
📊 Kết quả tìm kiếm: {'entries': [{'id': 'fUu2KrYRqJg', ...}]}
✅ Tìm thấy video ID: fUu2KrYRqJg
✅ URL: https://www.youtube.com/watch?v=fUu2KrYRqJg
```

### Cải Thiện Logging

Để xem rõ hơn, code có thể in ra toàn bộ entry:

```python
print(f"📊 Entry: {entry}")  # In toàn bộ thông tin
print(f"📊 Entry keys: {entry.keys()}")  # Xem có những key gì
print(f"📊 Video ID: {entry.get('id')}")  # Xem ID
```

## Cấu Trúc Dữ Liệu Chi Tiết

### Với `extract_flat=True` (Hiện Tại)

```python
entry = {
    'id': 'fUu2KrYRqJg',  # ✅ Luôn có
    'url': 'https://www.youtube.com/watch?v=fUu2KrYRqJg',  # ✅ Thường có
    'title': 'Hãy Trao Cho Anh',  # ⚠️ Có thể có hoặc không
    'duration': 225,  # ⚠️ Có thể có hoặc không
    # ... các thông tin khác
}
```

### Với `extract_flat=False` (Bị Block)

```python
entry = {
    'id': 'fUu2KrYRqJg',
    'title': 'Hãy Trao Cho Anh',  # ✅ Đầy đủ
    'uploader': 'Sơn Tùng M-TP',  # ✅ Đầy đủ
    'duration': 225,
    'view_count': 500000000,
    # ... rất nhiều thông tin
}
# Nhưng dễ bị block!
```

## Tại Sao Cần ID?

### 1. Build URL
```python
video_id = 'fUu2KrYRqJg'
url = f"https://www.youtube.com/watch?v={video_id}"
```

### 2. Lưu Trữ
```python
STREAM_TOKENS[token] = {
    "youtube_url": f"https://www.youtube.com/watch?v={video_id}",
    "video_id": video_id,  # Lưu ID để dùng sau
}
```

### 3. Hiển Thị
```python
title = f"YouTube Video {video_id}"  # "YouTube Video fUu2KrYRqJg"
```

## Kiểm Tra ID Có Tồn Tại Không?

### Trong Code Hiện Tại

```python
video_id = entry.get('id')  # Lấy ID
if video_id:  # Kiểm tra có ID không
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    return video_url
else:
    # Nếu không có ID, thử lấy URL trực tiếp
    video_url = entry.get('webpage_url') or entry.get('url')
```

### Debug Nếu Không Có ID

Nếu không có ID, có thể in ra để debug:

```python
if not video_id:
    print(f"⚠️ Không có video_id trong entry")
    print(f"📊 Entry keys: {list(entry.keys())}")
    print(f"📊 Entry: {entry}")
```

## Kết Luận

**Video ID được lấy từ:**
1. ✅ `entry.get('id')` - Từ kết quả tìm kiếm của yt-dlp
2. ✅ Hoặc extract từ URL nếu có sẵn

**Code hiện tại đã xử lý:**
- ✅ Lấy ID từ `entry.get('id')`
- ✅ Nếu không có ID, lấy URL từ `entry.get('webpage_url')`
- ✅ Build URL từ ID: `f"https://www.youtube.com/watch?v={video_id}"`

**Để xem ID trong logs:**
- Xem dòng: `✅ Tìm thấy video ID: fUu2KrYRqJg`
- Hoặc xem: `📊 Kết quả tìm kiếm: {...}`

