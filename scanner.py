import os
import json
import argparse
import re
from pathlib import Path

class RepoScanner:
    def __init__(self, repo_path, output_file=None):
        self.repo_path = Path(repo_path).resolve()
        self.output_file = output_file
        self.blueprint = {
            "name": self.repo_path.name,
            "tech_stack": [],
            "django_apps": [],
            "models": {},
            "go_routes": [],
            "structure": []
        }
        self.blacklist_names = {".git", "node_modules", "venv", "__pycache__", ".env", "credentials.json"}
        self.blacklist_extensions = {".pkl", ".xlsx", ".pdf", ".png", ".jpg", ".zip", ".log"}

    def scan(self, current_path, indent=0, max_depth=2):
        if indent > max_depth:
            return
        
        try:
            items = sorted(os.listdir(current_path))
            for item in items:
                item_path = current_path / item
                if item in self.blacklist_names or item.startswith(".") or item_path.suffix in self.blacklist_extensions:
                    continue
                prefix = "  " * indent + "├── "
                if item_path.is_dir():
                    self.blueprint["structure"].append(f"{prefix}{item}/")
                    self.scan(item_path, indent + 1, max_depth)
                else:
                    self.blueprint["structure"].append(f"{prefix}{item}")
        except PermissionError:
            pass

    def detect_tech_stack(self):
        if (self.repo_path / "manage.py").exists():
            self.blueprint["tech_stack"].append("Django")
            self._parse_django()
        if (self.repo_path / "backend/go.mod").exists() or (self.repo_path / "go.mod").exists():
            self.blueprint["tech_stack"].append("Go")
            self._parse_go()
        if (self.repo_path / "package.json").exists():
            self.blueprint["tech_stack"].append("Node.js/Frontend")

    def _parse_django(self):
        apps = [item.name for item in self.repo_path.iterdir() if item.is_dir() and (item / "apps.py").exists()]
        self.blueprint["django_apps"] = apps
        for app in apps:
            model_file = self.repo_path / app / "models.py"
            if model_file.exists():
                content = model_file.read_text()
                models = re.findall(r"class\s+(\w+)\(models\.Model\)", content)
                if models:
                    self.blueprint["models"][app] = models

    def _parse_go(self):
        # Scan backend/routes for Go route names
        routes_dir = self.repo_path / "backend" / "routes"
        if routes_dir.exists():
            self.blueprint["go_routes"] = [f.stem for f in routes_dir.glob("*.go")]

    def generate_markdown(self):
        md = []
        md.append(f"# REPO BLUEPRINT: {self.blueprint['name']}")
        md.append(f"\n## 🛠 TECH STACK: {', '.join(self.blueprint['tech_stack'])}")
        
        if self.blueprint["django_apps"]:
            md.append("\n### 📦 DJANGO APPS")
            md.append(", ".join(self.blueprint["django_apps"]))
            
            md.append("\n### 🏗 DATA MODELS (Django)")
            for app, models in self.blueprint["models"].items():
                md.append(f"- **{app}**: {', '.join(models)}")

        if self.blueprint["go_routes"]:
            md.append("\n### 🛣 GO ROUTES")
            md.append(", ".join(self.blueprint["go_routes"]))

        md.append("\n## 📂 DIRECTORY STRUCTURE (L2)")
        md.append("```")
        md.extend(self.blueprint["structure"])
        md.append("```")
        return "\n".join(md)

    def run(self):
        print(f"🚀 Scanning {self.repo_path}...")
        self.detect_tech_stack()
        self.scan(self.repo_path)
        output = self.generate_markdown()
        if self.output_file:
            with open(self.output_file, "w") as f:
                f.write(output)
            print(f"✅ Blueprint saved to {self.output_file}")
        else:
            print(output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--output")
    args = parser.parse_args()
    RepoScanner(args.path, args.output).run()
