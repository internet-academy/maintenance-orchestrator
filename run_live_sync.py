import os
import subprocess
import time
from pathlib import Path

# Configuration
WATCH_PATHS = [
    Path.home() / "ia/member",
    Path.home() / "ia/bohr-individual"
]
SYNC_SCRIPT = Path.home() / "projects/personal-agents/sync_blueprints.sh"
DEBOUNCE_SECONDS = 10

def run_sync(repo_name):
    print(f"🔔 Change detected in {repo_name}. Triggering surgical sync...")
    try:
        subprocess.run([str(SYNC_SCRIPT), repo_name], check=True)
        print(f"✅ {repo_name} Blueprint updated.")
    except Exception as e:
        print(f"❌ Sync failed: {e}")

def watch():
    print(f"👁️ Sentinel Watcher active on: {[str(p) for p in WATCH_PATHS]}")
    last_change = {}
    
    while True:
        try:
            for path in WATCH_PATHS:
                if not path.exists(): continue
                
                # Check for the most recently modified file in the repo
                # Focus on code files to avoid noise
                current_max = 0
                for root, dirs, files in os.walk(path):
                    if any(b in root for b in [".git", "node_modules", "venv", "__pycache__"]):
                        continue
                    for f in files:
                        if f.endswith(('.py', '.go', '.vue', '.ts', '.js')):
                            mtime = os.path.getmtime(os.path.join(root, f))
                            if mtime > current_max:
                                current_max = mtime
                
                repo_name = "member" if "member" in path.name else "bohr"
                
                # If a change is detected
                if current_max > last_change.get(repo_name, 0):
                    if last_change.get(repo_name, 0) != 0:
                        # Wait for the debounce period of silence
                        time.sleep(DEBOUNCE_SECONDS)
                        run_sync(repo_name)
                    last_change[repo_name] = current_max
            
            time.sleep(5) # Poll every 5 seconds
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Watcher Error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    watch()
