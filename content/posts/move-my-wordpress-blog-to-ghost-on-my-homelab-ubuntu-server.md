---
title: Move my Wordpress blog to Ghost on my homelab (Ubuntu Server)
date: '2025-12-03T03:08:57Z'
draft: false
description: 'This is a short how-to of what I did to move kientran.asia from Wordpress
  hosting to Ghost on my homelab. I focus on the essentials: migrate content, run
  Ghost in Docker…'
slug: move-my-wordpress-blog-to-ghost-on-my-homelab-ubuntu-server
tags:
- 🛠 Tools & Tech
categories:
- Startup
---

This is a short how-to of what I did to move kientran.asia from Wordpress hosting to Ghost on my homelab. I focus on the essentials: migrate content, run Ghost in Docker (Portainer), expose via Cloudflare Tunnel, and get SMTP working with Gmail so membership/invite emails work. Use it as a checklist or follow step-by-step.

Why I moved
-----------

Each year I spent ~1.5M VND on WordPress hosting, and I kept spending time on custom features. Ghost lets me focus on writing and subscriptions. It's simple, fast, and has built-in support for members and newsletters. So I migrated to a Ghost instance I control on my homelab.

Prerequites
-----------

* Ubuntu Server (homelab).
* Docker + Docker Compose and Portainer.
* Cloudflare account with Tunnel (Zero Trust).
* Domain (e.g. kientran.asia) managed in Cloudflare.
* Gmail account with 2-Step Verification enabled to create an App Password.
* A backup of your WordPress site.

How to do?
----------

### Step 1 - Export WordPress content to Ghost format

1. Try the Ghost/WordPress migrator plugin first. Install a WordPress plugin that exports to Ghost JSON (search "Ghost migrator" or "export to Ghost"). Export to a ghost-export.json if available.
2. If the plugin is not available, export WordPress content via WordPress Admin -> Tools > Export > All content to get wordpress.xml. Then convert XML > Ghost JSON using a converter tool (There are community tools that convert WordPress XML to Ghost JSON. Pick a maintained one or follow Ghost docs for migration.)
3. Save the final ghost-export.json file.

### Step 2 - Prepare the host directories

On your Ubuntu Server create the content folder that will be bind-mounted into Ghost.

```
sudo mkdir -p /opt/ghost/content
sudo chown -R 1000:1000 /opt/ghost/content
```

Ghost expects UID 1000 ownership for the content folder.

### Step 3 - Docker Compose stack (Portainer friendly)

Create a docker-compose.yml for Portainer or docker compose. This example users SQLite and includes Gmail SMTP placeholders.

```
version: '3.8'

services:
  ghost:
    image: ghost:latest
    container_name: ghost
    restart: unless-stopped
    ports:
      - "2368:2368"
    environment:
      url: https://your-domain.com
      database__client: sqlite3
      database__connection__filename: /var/lib/ghost/content/data/ghost.db
      mail__transport: SMTP
      mail__options__service: gmail
      mail__options__host: smtp.gmail.com
      mail__options__port: 587
      mail__options__secure: "false"
      mail__options__auth__user: "your-gmail"
      mail__options__auth__pass: "GMAIL_APP_PASSWORD_NO_SPACES"
    volumes:
      - /opt/ghost/content:/var/lib/ghost/content

volumes:
  ghost_data:
```

* Save this in /opt/ghost/docker-compose.yml or paste it into Portainer stack editor.
* Replace GMAIL\_APP\_PASSWORD\_NO\_SPACES with the 16-char Gmail App Password (no spaces).

Deploy the stack with Portainer or:

```
cd /opt/ghost
docker compose up -d
```

### Step 4 - Cloudflare Tunnel & domain mapping

I expose my homelab to the internet using Cloudflare Tunnel. Map the public hostname to the local service.

Example ingress for the tunnel config:

```
ingress:
  - hostname: kientran.asia
    service: http://127.0.0.1:2368
  - hostname: www.kientran.asia
    service: http_status:301
    # Or add a Page Rule redirect www -> non-www in Cloudflare dashboard
  - service: http_status:404
```

In Zero Trust Published Applications use internal URL http://127.0.0.1:2368 and set public hostname your-domain.com. Do not use 127.0.0.1 as the public hostname.

If you want www to redirect to root, add a Cloudflare Page Rule forwarding www.your-domain.com/\* -> https://your-domain.com/$1

### Step 5 - Gmail App Password for SMTP

1. Turn on 2-Step Verification on your Google account.
2. Go to Security –> App passwords in your Google account.
3. Create an App Password for Mail, name it "Ghost" and copy the 16 characters.
4. Paste the password into mail\_\_options\_\_auth\_\_pass in your stack, removing any spaces. Gmail shows spaces for readability. Use the raw 16 characters.

After updating docker-compose.yml in Portainer or on host, restart Ghost:

```
docker compose down
docker compose up -d
```

### Step 6 - Import content into Ghost

1. Open Ghost admin: https://kientran.asia/ghost. Create the initial owner account if prompted.
2. Admin → Labs → Import → Upload ghost-export.json. Ghost will import posts, pages, tags, and authors.
3. Check posts, images, and links. If images are still pointing to WordPress URLs, you can run a migration to copy images locally later or update URLs.

### Step 7 - Test members / invitations

1. Open Ghost admin: https://kientran.asia/ghost. Create the initial owner account if prompted.
2. Admin → Labs → Import → Upload ghost-export.json. Ghost will import posts, pages, tags, and authors.
3. Check posts, images, and links. If images are still pointing to WordPress URLs, you can run a migration to copy images locally later or update URLs.

```
docker logs ghost --since 1h
```

Common problems: wrong app password, incorrect port/secure settings, outbound network blocked by ISP.

### Useful fixes & notes

* If you created admin while testing with IP then switch to domain, you may need to clear browser cookies or log in again because cookies are domain-scoped.
* If you cannot log in and email is not available, you can reset the admin password by creating a bcrypt hash outside the container and updating the SQLite DB in /opt/ghost/content/data/ghost.db. Work carefully and backup first.
* Backup your content folder regularly:

```
tar czf /root/ghost-backup-$(date +%F).tar.gz /opt/ghost/content
```

* For production consider using MariaDB if you expect heavy load. For a simple personal blog SQLite is fine.

### **Final checklist before sharing**

* Domain DNS in Cloudflare is proxied (orange cloud) and Tunnel has published hostname kientran.asia.
* Ghost url env is https://your-domain.com
* Gmail App Password is pasted with no spaces.
* SMTP settings match port 587 + secure false (STARTTLS) or port 465 + secure true. I prefer 587 + STARTTLS.
* Invite test succeeded.
* Backups are in place.

This setup moved my blog from paid WordPress hosting to a Ghost instance I control. It reduced hosting cost and let me focus on writing. I hope these notes help you replicate the flow.
