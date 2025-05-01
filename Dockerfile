FROM alpine:latest

# Set proxy if needed
ENV HTTPS_PROXY="http://..."

# Install dependencies
RUN apk update && apk add --no-cache python3 py3-pip git nano busybox-suid bash samba-client

# Install Python packages
RUN pip install --break-system-packages ping3 netmiko loki-logger-handler requests

# Set working directory
WORKDIR /home

RUN mkdir -p /var/log

ARG cache_bust=1
# Clone your backup script repo
RUN git clone https://github.com/robrhce/Switch-Backup.git

# In case its cached
WORKDIR /home/Switch-Backup
RUN git pull

RUN chmod +x /home/Switch-Backup/archive.sh

CMD ["/home/Switch-Backup/archive.sh"]