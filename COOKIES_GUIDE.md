# 🍪 Hướng Dẫn Sử Dụng Cookies

## Tại Sao Cần Cookies?

YouTube đang block yt-dlp vì nghĩ đây là bot. Cookies giúp:
- ✅ YouTube nghĩ đây là bạn đang dùng (đã đăng nhập)
- ✅ Giảm đáng kể khả năng bị block
- ✅ Có thể download video dài hơn

## Cách Lấy Cookies

### Cách 1: Dùng Extension Browser (Dễ Nhất) ✅

#### Chrome/Edge:
1. Cài extension: **"Get cookies.txt LOCALLY"**
   - Link: https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc
2. Đăng nhập YouTube trên browser
3. Vào trang YouTube bất kỳ
4. Click extension → **"Export"**
5. Save file thành `cookies.txt`
6. Đặt file vào thư mục `music_server/`

#### Firefox:
1. Cài extension: **"cookies.txt"**
   - Link: https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/
2. Đăng nhập YouTube
3. Vào YouTube → Click extension → Export
4. Save thành `cookies.txt`

### Cách 2: Dùng yt-dlp (Tự Động)

```bash
# Export cookies từ Chrome
yt-dlp --cookies-from-browser chrome

# Hoặc từ Firefox
yt-dlp --cookies-from-browser firefox
```

Sau đó copy cookies vào file `cookies.txt`

### Cách 3: Manual (Phức Tạp)

1. Đăng nhập YouTube trên browser
2. Mở Developer Tools (F12)
3. Vào tab **Application** → **Cookies** → `https://www.youtube.com`
4. Copy các cookies quan trọng:
   - `__Secure-1PSID`
   - `__Secure-1PSIDTS`
   - `__Secure-3PSID`
   - `VISITOR_INFO1_LIVE`
   - `YSC`
5. Tạo file `cookies.txt` theo format Netscape

## Format File cookies.txt

File `cookies.txt` phải theo format Netscape:

```
# Netscape HTTP Cookie File
.youtube.com	TRUE	/	TRUE	1735689600	__Secure-1PSID	COOKIE_VALUE_HERE
.youtube.com	TRUE	/	TRUE	1735689600	__Secure-1PSIDTS	COOKIE_VALUE_HERE
```

## Cách Sử Dụng

1. **Export cookies** từ browser (dùng extension)
2. **Đặt file** `cookies.txt` vào thư mục `music_server/`
3. **Push lên GitHub** (hoặc không nếu muốn giữ private)
4. **Code sẽ tự động dùng** cookies khi có file

## Lưu Ý Bảo Mật

⚠️ **QUAN TRỌNG:**
- File `cookies.txt` chứa thông tin đăng nhập của bạn
- **KHÔNG commit** lên GitHub public repository
- Đã thêm `cookies.txt` vào `.gitignore`
- Chỉ dùng cho server riêng hoặc private repo

## Kiểm Tra Cookies Có Hoạt Động

Sau khi thêm cookies, logs sẽ không còn:
```
ERROR: Sign in to confirm you're not a bot
```

Thay vào đó sẽ thấy:
```
✅ Tải và chuyển đổi thành công!
```


