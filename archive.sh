#!/bin/sh

# Run the Python backup
python3 /home/Switch-Backup/multivendor_run.py

# SMB share details
#SMB_SHARE="//192.168.1.100/backups"
#SMB_USER="admin"
#SMB_PASS="password"
LOCAL_DIR="/home/Switch-Backup/backup-config"
ARCHIVE_DIR="/home/Switch-Backup/archive"

mkdir -p "$ARCHIVE_DIR"

for f in "$LOCAL_DIR"/*; do
    [ -f "$f" ] || continue
    echo smbclient "$SMB_SHARE" -U "${SMB_USER}%${SMB_PASS}" -c "put $f" && \
    mv "$f" "$ARCHIVE_DIR/"
done