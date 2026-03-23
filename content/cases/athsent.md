---
title: "Athsent – AI Video Safety"
description: "Edge AI detect hazard realtime trên công trường. Giảm incidents, deploy nhanh nhiều site."
---
# Athsent – AI Video Safety

## Vấn đề
Công trường cần detect hazard (vật cản, hành vi nguy hiểm, thiết bị thiếu) theo thời gian thực. Làm thủ công tốn người, chậm phản hồi và khó mở rộng.

## Giải pháp
- Edge AI integration (YOLO + custom model) chạy gần nguồn dữ liệu.
- Pipeline nhận video → detect → alert real-time qua Telegram/app.
- Workflow automation để tổng hợp log, phân loại sự cố và báo cáo cho quản lý.

## Kết quả (metrics)
- Giảm ~40% incidents so với baseline vận hành thủ công.
- Deploy 10 sites, latency < 1s (tuỳ điều kiện mạng tại site).
- Giảm thời gian xử lý sự cố nhờ alert đúng ngữ cảnh.

## Tech stack
Python/JS, N8N notify, VPS edge, dashboard báo cáo nội bộ.

## Nếu bạn muốn làm tương tự
[Book free audit](/contact/) để mình review dữ liệu hiện tại và đề xuất roadmap trong 2-4 tuần.

