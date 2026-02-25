import os
import json
import argparse
from pathlib import Path

class RepoScanner:
    def __init__(self, repo_path, output_file=None):
        self.repo_path = Path(repo_path).resolve()
        self.output_file = output_file
        self.blueprint = {
            "name": self.repo_path.name,
            "structure": {},
            "tech_stack": [],
            "key_files": [],
            "api_endpoints": [],
            "models": []
        }
        self.blacklist = {".git", "node_modules", "venv", "__pycache__", ".env", "credentials.json", ".pkl"}

    def scan_structure(self, current_path, depth=0, max_depth=2):
        if depth > max_depth:
            return {}
        
        structure = {}
        try:
            for item in os.listdir(current_path):
                if item in self.blacklist or item.startswith("."):
                    continue
                
                item_path = current_path / item
                if item_path.is_dir():
                    structure[item] = self.scan_structure(item_path, depth + 1, max_depth)
                else:
                    structure[item] = "file"
        except PermissionError:
            pass
        return structure

    def detect_tech_stack(self):
        if (self.repo_path / "manage.py").exists():
            self.blueprint["tech_stack"].append("Django")
        if (self.repo_path / "backend/go.mod").exists() or (self.repo_path / "go.mod").exists():
            self.blueprint["tech_stack"].append("Go")
        if (self.repo_path / "package.json").exists():
            self.blueprint["tech_stack"].append("Node.js/Frontend")

    def run(self):
        print(f"🚀 Scanning {self.repo_path}...")
        self.detect_tech_stack()
        self.blueprint["structure"] = self.scan_structure(self.repo_path)
        
        # Save or Print
        output = self.generate_markdown()
        if self.output_file:
            with open(self.output_file, "w") as f:
                f.write(output)
            print(f"✅ Blueprint saved to {self.output_file}")
        else:
            print(output)

    def generate_markdown(self):
        md = [f"# REPO BLUEPRINT: {self.blueprint['name']}
"]
        md.append(f"## 🛠 TECH STACK: {', '.join(self.blueprint['tech_stack'])}
")
        md.append("## 📂 DIRECTORY STRUCTURE (L2)")
        md.append("```")
        md.append(self._format_structure(self.blueprint["structure"]))
        md.append("```
")
        return "
".join(md)

    def _format_structure(self, structure, indent=0):
        lines = []
        for name, content in structure.items():
            prefix = "  " * indent + "├── "
            if isinstance(content, dict):
                lines.append(f"{prefix}{name}/")
                lines.extend(self._format_structure(content, indent + 1))
            else:
                lines.append(f"{prefix}{name}")
        return "
".join(lines)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a Repo Blueprint.")
    parser.add_argument("path", help="Path to the repository")
    parser.add_argument("--output", help="Output Markdown file")
    args = parser.parse_args()

    scanner = RepoScanner(args.path, args.output)
    scanner.run()
