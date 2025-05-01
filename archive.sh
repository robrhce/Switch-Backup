#!/bin/sh


set -x
set -e




# SMB share details
#SMB_SHARE="//192.168.1.100/backups"
#SMB_USER="admin"
#SMB_PASS="password"
MODE=${MODE:-once}  # Default to "once" if not set
LOCAL_DIR="/home/Switch-Backup/backup-config"
ARCHIVE_DIR="/home/Switch-Backup/archive"
LINK_PATH="/etc/periodic/daily/archive.sh"

# Run the Python backup script
run_backup() {
    echo "[INFO] Running backup script..."
    python3 /home/Switch-Backup/multivendor_run.py
}

# Upload and archive files
upload_and_archive() {
    echo "[INFO] Uploading and archiving backup files..."
    mkdir -p "$ARCHIVE_DIR"

    for f in "$LOCAL_DIR"/*; do
        [ -f "$f" ] || continue
        fname=$(basename "$f")
        smbclient "$SMB_SHARE" -U "${SMB_USER}" --password "${SMB_PASS}" -c "put \"$f\" \"$fname\" " && \
        mv "$f" "$ARCHIVE_DIR/"
    done
}

# Execute the job
    run_backup
    upload_and_archive


# If we're PID 1, we're the container's main process
if [ "$MODE" = "daily" ] && [ "$$" -eq 1 ]; then
    echo "[INFO] Setting up for daily cron execution..."

    if [ ! -L "$LINK_PATH" ]; then
        echo "[INFO] Linking script to $LINK_PATH"
        ln -s /usr/local/bin/archive.sh "$LINK_PATH"
    fi

    echo "[INFO] Starting crond..."
    exec crond -f
else
    echo "[INFO] Execution finished. Exiting."
    exit 0
fi