---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date.Format "2006-01-02T15:04:05Z07:00" }}
draft: true
# Meta SEO (~150–160 ký tự): tóm tắt cho Google / mạng xã hội. Để trống = Hugo tự tóm tắt từ nội dung.
description: ""
# Tùy chọn: tiêu đề tab khác với title bài (nếu cần nhồi từ khóa ngắn). Mặc định dùng title.
# seo_title: ""
# slug: chỉ thêm khi cần URL khác tên file; mặc định Hugo lấy slug từ tên file (.md).
categories:
  - Essays
tags: []
---

Lead with the claim or question the essay answers.
