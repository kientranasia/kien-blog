---
title: Dùng AI tạo ra ChatBot()
date: '2023-02-09T22:00:42Z'
draft: false
description: Hiện tại mọi người không còn lạ gì với ChatGPT nữa. Mình cũng đang sử
  dụng ChatGPT phục vụ công việc của mình chủ yếu là research, gợi ý. mình cũng tò
  mò không biết giới…
slug: dung-ai-tao-ra-chatbot
tags:
- 📔 Journal
categories:
- Essays
---

Hiện tại mọi người không còn lạ gì với ChatGPT nữa. Mình cũng đang sử dụng ChatGPT phục vụ công việc của mình chủ yếu là research, gợi ý. mình cũng tò mò không biết giới hạn của ChatGPT ở đâu? Liệu nó sẽ phụ thuộc vào ChatGPT hay phụ thuộc vào người sử dụng nó.

Tại Việt Nam đã có một ứng dụng tiên phong sử dụng ChatGPT đó là VoiceGPT đến từ Tesse nhằm đưa giải pháp ChatGPT đến cho mọi người, tranh thủ lúc làm việc xong mình muốn relax bản thân, mình dùng ChatGPT để thử tạo ra một con ChatBot để tự động tạo nội dung đăng tải lên nền tảng mạng xã hội.

ChatBot mình sẽ dùng hoàn toàn từ gợi ý của ChatGPT. Mình cũng sẽ chỉnh sửa lại nếu code không hoạt động. Hiện mình sẽ giao tiếp được với OpenAI qua engine=”text-davinci-002″. Mình chưa thử test với version 3. Nhưng sẽ có rất nhiều điểm khác biệt và phải tốn bao chi phí.

So sánh giữa 2 version: [How do text-davinci-002 and text-davinci-003 differ? | OpenAI Help Center](https://help.openai.com/en/articles/6779149-how-do-text-davinci-002-and-text-davinci-003-differ)

Thôi vào việc:

Code được cung cấp từ ChatGPT:

```
import openai

openai.api_key = "your api key"
# api key mình lấy trực tiếp tờ OpenAI

def chatbot():
    while True:
        user_input = input("You: ")
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt="ChatGPT: " + user_input,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        ).choices[0].text
        print(response)

if __name__ == "__main__":
    chatbot()
```

Tadar và Kết quả: Đoạn code trên mình dùng trực tiếp không chỉnh sửa. Next step mình sẽ build ChatBot tự tạo content mỗi ngày và một chatbot kết nối với các nền tảng mạng xã hội của mình để cập nhật các nội dung đó lên MXH.

![](__GHOST_URL__/content/images/wordpress/2023/02/Screenshot-2023-02-09-214427-1024x576.png)

Kết quả khi mới gọi vài dòng lệnh thì mình đã tốn 0.03$ trên 18$ được sử dụng miễn phí.

![](__GHOST_URL__/content/images/wordpress/2023/02/832E4C57-6FB2-44A9-90BD-6628A7E1AA8B-1024x768.jpeg)

Do phía API từ Twitter vẫn chưa cho phép mình sử dụng API nên mình chưa thể test code tự đăng bài viết được, nhưng khi review code được cung cấp từ ChatGPT so với hướng dẫn từ thư viện thì mình thấy code có thể chạy trực tiếp được. Không cần chỉnh sửa =))

Bạn còn đợi gì nữa? Hãy ứng dụng AI, công nghệ vào cuộc sống, kinh doanh của mình nào.
