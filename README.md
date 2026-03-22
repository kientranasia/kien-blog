# kien-blog

Personal essay blog: **Hugo** (site), **Decap CMS** (admin at `/admin/`), **GitHub** (content), **GitHub Actions** (build + container publish), **Docker + nginx** (runtime).

Viết lâu dài, categories, draft vs public: xem **[HUONG-DAN-BLOG.md](HUONG-DAN-BLOG.md)** (file hướng dẫn nội bộ).

## Local preview

```bash
hugo server --buildDrafts --disableFastRender
```

Open <http://localhost:1313/> and <http://localhost:1313/admin/>.

## First-time configuration

1. **`baseURL`** — Trong `hugo.yaml` đang dùng **`https://kientran.asia/`** (canonical, Open Graph, RSS, sitemap). Xem thêm `enableRobotsTXT` và `sitemap` trong cùng file.
   - **Đổi domain:** sửa `baseURL` trong `hugo.yaml` (và `static/admin/config.yml` nếu dùng Decap).
   - **Preview local:** `hugo server` dùng host dev; không cần truyền `--baseURL` trừ khi bạn muốn ép URL.

2. **Decap + GitHub** — Edit `static/admin/config.yml`:
   - Set `backend.repo` to `your-username/your-repo`.
   - Confirm `branch` matches your default branch.

3. **GitHub OAuth for Decap** (production admin login):
   - GitHub → Settings → Developer settings → OAuth Apps → New.
   - **Homepage URL**: your site origin, e.g. `https://blog.example.com`.
   - **Authorization callback URL**: `https://api.netlify.com/auth/dash` only applies when using Netlify Identity. For a **self-hosted** stack, use a small auth endpoint or Decap’s recommended proxy. Common options:
     - **Netlify** with [Decap + GitHub](https://decapcms.org/docs/github-backend/) (easiest OAuth story), or
     - **`netlify-cms-github-backend`**-compatible proxy / serverless function that exchanges the code for a token (see [Decap backend docs](https://decapcms.org/docs/github-backend/)).
   - If you only edit locally for now, set `local_backend: true` at the top of `config.yml` and run:
     ```bash
     npx decap-server
     ```
     while the Hugo dev server is running.

4. **Container** — On push to `main`, the workflow runs `hugo --minify`, builds the image, and pushes to `ghcr.io/<user>/<repo>:latest` (and a `:sha-*` tag).

   Run locally after a build:

   ```bash
   hugo --minify
   docker build -t kien-blog:local .
   docker run --rm -p 8080:80 kien-blog:local
   ```

   Then open <http://localhost:8080/>.

## New essay from CLI

```bash
hugo new content posts/my-essay-title.md
```

## Deploy
```
cd /path/to/kien-blog

cat > .env <<'EOF'
OAUTH_GITHUB_CLIENT_ID=your_client_id
OAUTH_GITHUB_CLIENT_SECRET=your_client_secret
EOF

docker compose up -d --pull always


---
cd ~/homelab/kien-blog
git pull

hugo --minify --config hugo.yaml

docker compose up -d --build --force-recreate
docker compose ps
docker compose logs web --tail=80
```

Edit front matter (`draft`, `description`, `slug`, `tags`) and body; commit and push.



## Auto build
1) Trên server, kéo code mới (repo đã có sẵn `auto-deploy.sh`) và đảm bảo file có quyền chạy:
```bash
cd ~/homelab/kien-blog
git pull
chmod +x auto-deploy.sh
```

2) Cài cron chạy tự động (mỗi 2 phút)
crontab -e
Thêm dòng:

*/2 * * * * /home/kientran/homelab/kien-blog/auto-deploy.sh >/tmp/kien-blog-auto-deploy.log 2>&1
3) Lưu trữ log build
- Script sẽ ghi lịch sử vào `.build-history.log` trong thư mục repo.
- Lúc cron chạy vẫn ghi vào `/tmp/kien-blog-auto-deploy.log` như bạn set ở trên.

4) Test nhanh
Publish một bài mới trên Decap (draft = OFF).
Chờ 1–2 phút.

## Stack rationale

| Piece | Role |
|--------|------|
| Hugo | Fast static HTML, good defaults for SEO and RSS. |
| Decap | Browser UI for Markdown without teaching non-devs Git. |
| Git | Source of truth; reviews and history on real files. |
| Actions | Reproducible build; no manual `hugo` on deploy day. |
| Docker | One artefact (nginx + `public/`) to run anywhere. |

## Licence

MIT (theme and scaffolding in this repo).
