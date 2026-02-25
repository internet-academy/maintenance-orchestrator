# Gemini Auto-Sync: Replication Guide (Desktop/Laptop)

This guide ensures your machines stay in perfect sync using the `gemini-sync.service`.

## 1. Prerequisites
Install the monitoring tools:
```bash
sudo apt update && sudo apt install inotify-tools
```

## 2. Path Standardization
The system expects `personal-agents` to live in `~/projects/`. If you have it elsewhere, move it or link it:
```bash
# Ensure the parent directory exists
mkdir -p ~/projects
mkdir -p ~/projects

# If your repo is currently in ~/projects/personal-agents:
mv ~/projects/personal-agents ~/projects/
ln -s ~/projects/personal-agents ~/projects/personal-agents
```

## 3. Install the Service
Create the systemd user directory if it doesn't exist:
```bash
mkdir -p ~/.config/systemd/user/
```

Copy the service definition (run this from your terminal):
```bash
cat << 'EOF' > ~/.config/systemd/user/gemini-sync.service
[Unit]
Description=Gemini Auto-Sync Service
After=network.target

[Service]
ExecStart=/home/min/projects/watcher.sh
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
EOF
```

## 4. Activate
```bash
systemctl --user daemon-reload
systemctl --user enable gemini-sync.service
systemctl --user start gemini-sync.service
```

## 5. Verify
Check the logs to ensure it's watching your folders:
```bash
journalctl --user -u gemini-sync.service -f
```

---
*Note: The `watcher.sh` and `sync-all.sh` scripts are already located in `~/projects/` and are synced via Git. If they are missing on a new machine, clone `projects` first.*
