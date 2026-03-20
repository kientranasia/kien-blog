# kien-blog

Personal essay blog: **Hugo** (site), **Decap CMS** (admin at `/admin/`), **GitHub** (content), **GitHub Actions** (build + container publish), **Docker + nginx** (runtime).

Viết lâu dài, categories, draft vs public: xem **[HUONG-DAN-BLOG.md](HUONG-DAN-BLOG.md)** (file hướng dẫn nội bộ).

## Local preview

```bash
hugo server --buildDrafts --disableFastRender
```

Open <http://localhost:1313/> and <http://localhost:1313/admin/>.

## First-time configuration

1. **`baseURL`** — Mặc định trong `hugo.yaml` là `/` + `relativeURLs: true` (không gắn domain giả). Khi đã có domain ổn định:
   - **Build local / CI có URL tuyệt đối:** `hugo --minify --baseURL "https://blog.example.com/"`  
   - **GitHub Actions:** đặt biến repo **`HUGO_BASEURL`** (Settings → Secrets and variables → Actions → Variables), workflow sẽ truyền vào Hugo.

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
```

Edit front matter (`draft`, `description`, `slug`, `tags`) and body; commit and push.

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
