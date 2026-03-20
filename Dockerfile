# Runtime image: serves pre-built Hugo output from ./public
# GitHub Actions runs `hugo --minify` then `docker build`.
FROM nginx:1.27-alpine

COPY nginx/default.conf /etc/nginx/conf.d/default.conf
COPY public /usr/share/nginx/html

EXPOSE 80
