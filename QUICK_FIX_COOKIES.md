# ⚡ Quick Fix: Xóa Cookies Khỏi Git

## ✅ Đã Làm

1. ✅ Đổi tên `cookies.txt.txt` → `cookies.txt`
2. ✅ Thêm `cookies.txt.txt` vào `.gitignore`
3. ✅ Đảm bảo `.gitignore` có cả 2 file

## 🔧 Cần Làm Tiếp

### Nếu File Đã Được Commit:

```bash
# Xóa khỏi git (nhưng giữ file local)
git rm --cached cookies.txt
git rm --cached cookies.txt.txt

# Commit
git commit -m "Remove cookies from git (security)"

# Push
git push origin main
```

### Nếu File Chưa Được Commit:

✅ **Không cần làm gì!** File đã được `.gitignore` bảo vệ.

## Kiểm Tra

Chạy lệnh này để kiểm tra:
```bash
git status cookies.txt
```

Nếu thấy:
- `nothing to commit` → ✅ An toàn!
- `new file: cookies.txt` → Cần xóa khỏi git (dùng `git rm --cached`)

## Lưu Ý

- ⚠️ Nếu đã push lên GitHub → Cần xóa khỏi git history
- ✅ File vẫn ở local, code vẫn dùng được
- ✅ Xem `FIX_COOKIES_GIT.md` để biết cách xóa khỏi history

