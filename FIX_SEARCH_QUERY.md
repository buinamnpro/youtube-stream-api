# 🔧 Fix: YouTube Search Query Format

## Vấn Đề

Từ logs, tôi thấy:
```
[generic] Trích xuất URL: nhac
'extractor': 'generic'  ← Đang dùng generic extractor!
'url': 'ytsearch1:nhac'  ← Không parse được
⚠️ Không có mục nào trong kết quả
```

**Vấn đề:** yt-dlp không nhận diện đây là YouTube search, nên dùng generic extractor.

## Nguyên Nhân

### Trước Đây (Sai):
```python
ydl_opts = {
    'default_search': 'ytsearch1',  # ← Không hoạt động đúng
}
info = ydl.extract_info(query, download=False)  # query = "nhac"
```

→ yt-dlp không biết đây là YouTube search, dùng generic extractor.

### Sau Khi Sửa (Đúng):
```python
search_query = f"ytsearch1:{query}"  # "ytsearch1:nhac"
ydl_opts = {
    # Không cần default_search nữa
}
info = ydl.extract_info(search_query, download=False)  # search_query = "ytsearch1:nhac"
```

→ yt-dlp nhận diện đúng là YouTube search!

## Giải Pháp Đã Áp Dụng

### 1. Format Query Trực Tiếp
```python
search_query = f"ytsearch1:{query}"  # "ytsearch1:nhac"
```

### 2. Bỏ `default_search`
- Không cần `default_search` nữa
- Format query trực tiếp trong code

### 3. Thêm Logging
```python
print(f"🔍 Query formatted: '{search_query}'")
```

## Kết Quả Mong Đợi

Sau khi deploy, logs sẽ hiển thị:
```
🔍 Đang tìm kiếm: 'nhac'
🔍 Query formatted: 'ytsearch1:nhac'
[youtube:search] Trích xuất URL: ytsearch1:nhac  ← Đúng extractor!
📊 Kết quả tìm kiếm: {'entries': [{'id': 'fUu2KrYRqJg', ...}]}
✅ Tìm thấy video ID: fUu2KrYRqJg
```

## Test

Sau khi deploy, test:
```
https://music-server-cdfv.onrender.com/get_audio_url?q=nhac
```

## Lưu Ý

- `ytsearch1:` là prefix bắt buộc để yt-dlp nhận diện YouTube search
- Số `1` nghĩa là lấy 1 video đầu tiên
- Có thể dùng `ytsearch5:` để lấy 5 video

