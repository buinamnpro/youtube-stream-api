# 🔒 Xóa Cookies Khỏi Git History

## ⚠️ QUAN TRỌNG: File cookies.txt chứa thông tin đăng nhập!

Nếu bạn đã commit file cookies.txt lên GitHub public, cần xóa ngay!

## Cách Xóa File Khỏi Git

### Bước 1: Xóa File Khỏi Git (Nhưng Giữ File Local)

```bash
cd music_server
git rm --cached cookies.txt
```

Hoặc nếu file tên là `cookies.txt.txt`:
```bash
git rm --cached cookies.txt.txt
```

### Bước 2: Commit Thay Đổi

```bash
git commit -m "Remove cookies.txt from git (security)"
git push origin main
```

### Bước 3: Xóa Khỏi Git History (Nếu Đã Commit Trước Đó)

⚠️ **CẢNH BÁO:** Lệnh này sẽ rewrite git history!

```bash
# Xóa file khỏi toàn bộ git history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch cookies.txt cookies.txt.txt" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (cẩn thận!)
git push origin --force --all
```

**Hoặc dùng BFG Repo-Cleaner (Dễ hơn):**

1. Download BFG: https://rtyley.github.io/bfg-repo-cleaner/
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
```

Nếu không có kết quả → Đã xóa thành công!

## Đảm Bảo .gitignore Đúng

File `.gitignore` đã có:
```
cookies.txt
*.cookies
```

## Lưu Ý

- ⚠️ Nếu đã push lên GitHub public, cookies có thể đã bị lộ
- ✅ Nên đổi password YouTube sau khi xóa
- ✅ File cookies.txt vẫn tồn tại local (không bị xóa)
- ✅ Chỉ bị xóa khỏi git repository

## Sau Khi Xóa

1. ✅ File cookies.txt vẫn ở local
2. ✅ Code vẫn dùng được cookies
3. ✅ Không còn trong git repository
4. ✅ Không ai có thể thấy cookies trên GitHub


