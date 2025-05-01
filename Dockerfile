FROM alpine:latest

# Set proxy if needed
ENV HTTPS_PROXY="http://10.18.241.11:3128"

# Install dependencies
RUN apk update && apk add --no-cache python3 py3-pip git nano busybox-suid bash

# Install Python packages
RUN pip install --break-system-packages ping3 netmiko loki-logger-handler requests

# Set working directory
WORKDIR /home

# Clone your backup script repo
RUN git clone https://github.com/robrhce/Switch-Backup.git

# Add a cron job script in /etc/periodic/daily
RUN printf '#!/bin/sh \n cd /home/Switch-Backup \n python3 /home/Switch-Backup/multivendor_run.py \n' > /etc/periodic/daily/switch-backup \
    && chmod +x /etc/periodic/daily/switch-backup

# Create log directory
RUN mkdir -p /var/log

# Start cron in foreground (default CMD)
CMD ["crond", "-f"]