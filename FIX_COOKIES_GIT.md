# 🔒 Xóa Cookies Khỏi Git (QUAN TRỌNG!)

## ⚠️ CẢNH BÁO BẢO MẬT

File `cookies.txt` hoặc `cookies.txt.txt` chứa thông tin đăng nhập YouTube của bạn!
**Nếu đã commit lên GitHub public → Cần xóa ngay!**

## Các Bước Xóa

### Bước 1: Xóa File Khỏi Git (Nhưng Giữ Local)

```bash
cd music_server

# Xóa cả 2 file nếu có
git rm --cached cookies.txt
git rm --cached cookies.txt.txt
```

### Bước 2: Commit Thay Đổi

```bash
git commit -m "Remove cookies.txt from git (security)"
git push origin main
```

### Bước 3: Kiểm Tra .gitignore

Đảm bảo `.gitignore` có:
```
cookies.txt
cookies.txt.txt
*.cookies
```

✅ **Đã có rồi!**

### Bước 4: Xóa Khỏi Git History (Nếu Đã Commit Trước Đó)

⚠️ **CẢNH BÁO:** Lệnh này sẽ rewrite git history!

```bash
# Xóa file khỏi toàn bộ git history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch cookies.txt cookies.txt.txt" \
  --prune-empty --tag-name-filter cat -- --all

# Force push
git push origin --force --all
```

**Hoặc dùng BFG Repo-Cleaner (Dễ hơn):**

1. Download: https://rtyley.github.io/bfg-repo-cleaner/
2. Chạy:
```bash
java -jar bfg.jar --delete-files cookies.txt
java -jar bfg.jar --delete-files cookies.txt.txt
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push origin --force --all
```

## Kiểm Tra

Sau khi xóa, kiểm tra:
```bash
git log --all --full-history -- cookies.txt
git log --all --full-history -- cookies.txt.txt
```

Nếu không có kết quả → ✅ Đã xóa thành công!

## Lưu Ý Quan Trọng

- ⚠️ **Nếu đã push lên GitHub public**, cookies có thể đã bị lộ
- ✅ **Nên đổi password YouTube** sau khi xóa
- ✅ File cookies.txt vẫn tồn tại local (không bị xóa)
- ✅ Chỉ bị xóa khỏi git repository
- ✅ Code vẫn dùng được cookies local

## Sau Khi Xóa

1. ✅ File cookies.txt vẫn ở local
2. ✅ Code vẫn dùng được cookies
3. ✅ Không còn trong git repository
4. ✅ Không ai có thể thấy cookies trên GitHub

## Quick Commands

```bash
# Xóa khỏi git (giữ file local)
git rm --cached cookies.txt cookies.txt.txt

# Commit
git commit -m "Remove cookies from git"

# Push
git push origin main
```


