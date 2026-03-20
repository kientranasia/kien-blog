# Hướng dẫn viết & bố trí blog (cho chủ site)

Tài liệu nội bộ: cách dùng **categories**, **draft**, Decap, và khi nào nên tách thêm mục. Khách đọc không cần file này.

## `baseURL` và domain

- Repo mặc định dùng `baseURL: /` và `relativeURLs: true` — link trong HTML là đường dẫn tương đối, không cần placeholder domain.
- Khi cần **canonical / RSS đúng domain**, build với:  
  `hugo --minify --baseURL "https://domain-cua-ban.com/"`  
  hoặc biến **`HUGO_BASEURL`** trên GitHub Actions (xem README).

## Categories và trang `/categories/<trụ>/`

- Hugo chỉ tạo trang riêng cho một trụ khi có **ít nhất một bài không phải `draft: true`** gắn `categories` đó.
- Khi chưa có bài public, link trụ có thể 404 — bình thường.
- Danh sách tổng trên site: đường dẫn `/categories/`.

## Gợi ý khi kho bài lớn dần

- Mỗi bài nên có **một `category` chính** (gọn URL, dễ lọc); dùng **`tags`** cho nhánh phụ.
- Tiêu đề và `description` trong front matter nên rõ — bạn sẽ cảm ơn mình sau vài năm.

## Gợi ý tách thêm mục (khi đủ bài)

Chỉ cân nhắc khi một trụ có ~10–15 bài và cảm giác “kẹt”:

| Gợi ý | Gần trụ nào | Khi nào tách |
|--------|----------------|--------------|
| **Systems** | Startup + Philosophy | Quy trình, kiến trúc thông tin, tự động hóa “xương sống” |
| **Craft** | Startup + Life | Kỹ năng làm nghề, chuẩn nghề, tay nghề tư vấn |
| **Money & risk** | Startup + Philosophy | Giá, hợp đồng, quyết định tài chính |
| **Family & care** | Life + Happy | Trách nhiệm, thời gian, ranh giới |
| **Learning log** | Philosophy + Life | Sách, khóa, mentor — *có kết luận áp dụng* |

Để thêm taxonomy mới: khai báo trong `hugo.yaml`, rồi dùng trong front matter và (nếu cần) chỉnh Decap `static/admin/config.yml`.

## Viết bài nhanh (CLI)

```bash
hugo new content posts/ten-bai.md
```

Chỉnh `draft`, `description`, `slug`, `categories`, `tags`, rồi commit.

## Decap CMS (`/admin/`)

- Cấu hình repo: `static/admin/config.yml` → `backend.repo`, `branch`.
- OAuth GitHub cho môi trường production: xem [README](README.md).
- Local: có thể bật `local_backend: true` và chạy `npx decap-server` cùng lúc với `hugo server`.

## Build production và draft

- `hugo --minify`: **không** đưa draft vào bản phát hành.
- `hugo server --buildDrafts`: xem nháp khi dev.
