FROM alpine:latest

# Set proxy if needed
ENV HTTPS_PROXY="http://..."

# Install dependencies
RUN apk update && apk add --no-cache python3 py3-pip git nano busybox-suid bash samba-client

# Install Python packages
RUN pip install --break-system-packages ping3 netmiko loki-logger-handler requests

# Set working directory
WORKDIR /home

# Clone your backup script repo
RUN git clone https://github.com/robrhce/Switch-Backup.git

# Add a cron job script in /etc/periodic/daily
RUN cp /home/Switch-Backup/archive.sh /etc/periodic/daily/archive.sh

RUN chmod +x /etc/periodic/daily/archive.sh

# Create log directory
RUN mkdir -p /var/log

# Start cron in foreground (default CMD)
CMD ["crond", "-f"]