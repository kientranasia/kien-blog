---
title: "Why a static blog still wins"
date: 2025-03-20T09:00:00Z
draft: false
description: "A short anchor post explaining the stack and tone of this site."
slug: why-static-blog-wins
categories:
  - Essays
tags:
  - meta
  - hugo
---

For a personal site, you want three things at once: pages that load instantly, URLs that search engines understand, and a workflow that does not get between you and publishing. Static generators like Hugo give you the first two by default. Pair them with Git-backed content and a small admin UI, and you get a system that is boring in the best way.

This blog is intentionally **essay-first**. Posts assume you might read them start to finish, not skim cards in a feed. Typography and spacing favour long paragraphs, block quotes, and the occasional code sample when automation or implementation details matter.

The admin UI runs at `/admin/` and writes Markdown into this repository. Deployment is automated: push to the main branch, and the pipeline builds the site and packages it for Docker so the public site is always in sync with what is in Git—no manual rebuild on a laptop.

Để đặt domain cho RSS/canonical khi đã có host cố định, xem `README.md` (biến môi trường `HUGO_BASEURL` khi build). Decap: sửa `static/admin/config.yml` và OAuth theo README.
