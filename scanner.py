import os
import json
import argparse
import re
import ast
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
            "relationships": [],
            "go_routes": [],
            "api_calls": [],
            "structure": []
        }
        self.blacklist_names = {".git", "node_modules", "venv", "__pycache__", ".env", "credentials.json"}
        self.blacklist_extensions = {".pkl", ".xlsx", ".pdf", ".png", ".jpg", ".zip", ".log"}

    def scan(self, current_path, indent=0, max_depth=2):
        try:
            items = sorted(os.listdir(current_path))
            for item in items:
                item_path = current_path / item
                if item in self.blacklist_names or item.startswith(".") or item_path.suffix in self.blacklist_extensions:
                    continue
                
                if indent <= max_depth:
                    prefix = "  " * indent + "├── "
                    if item_path.is_dir():
                        self.blueprint["structure"].append(f"{prefix}{item}/")
                    else:
                        self.blueprint["structure"].append(f"{prefix}{item}")

                if item_path.is_dir():
                    self.scan(item_path, indent + 1, max_depth)
                else:
                    if item_path.suffix in {".vue", ".ts", ".js"}:
                        self._extract_api_calls(item_path)
        except PermissionError:
            pass

    def _extract_api_calls(self, file_path):
        try:
            content = file_path.read_text()
            urls = re.findall(r"(?:apiRequest|get|post|put|delete|patch)\s*\(?\s*['\"](/[\w/_-]+)['\"]", content)
            imports = re.findall(r"import\s+{[^}]+}\s+from\s+['\"](@/api/[^'\"]+|../api/[^'\"]+)['\"]", content)
            
            if urls or imports:
                res = {}
                if urls: res["urls"] = list(set(urls))
                if imports: res["imports"] = list(set(imports))
                self.blueprint["api_calls"].append({file_path.name: res})
        except Exception:
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
                try:
                    tree = ast.parse(model_file.read_text())
                    for node in ast.walk(tree):
                        if isinstance(node, ast.ClassDef):
                            model_name = node.name
                            fields = []
                            for subnode in ast.walk(node):
                                if isinstance(subnode, ast.Assign) and isinstance(subnode.value, ast.Call):
                                    func_name = ""
                                    if hasattr(subnode.value.func, 'attr'):
                                        func_name = subnode.value.func.attr
                                    elif hasattr(subnode.value.func, 'id'):
                                        func_name = subnode.value.func.id
                                        
                                    if func_name in ['ForeignKey', 'OneToOneField', 'ManyToManyField']:
                                        if subnode.value.args and isinstance(subnode.value.args[0], (ast.Constant, ast.Str)):
                                            target = subnode.value.args[0].s if hasattr(subnode.value.args[0], 's') else subnode.value.args[0].value
                                            self.blueprint["relationships"].append(f"{app}.{model_name} -> {target}")
                                    
                                    if isinstance(subnode.targets[0], ast.Name):
                                        fields.append(subnode.targets[0].id)
                            
                            if fields:
                                self.blueprint["models"][f"{app}.{model_name}"] = fields[:10]
                except Exception:
                    pass

    def _parse_go(self):
        routes_dir = self.repo_path / "backend" / "routes"
        if not routes_dir.exists():
            routes_dir = self.repo_path / "routes"
        if routes_dir.exists():
            for f in routes_dir.glob("*.go"):
                content = f.read_text()
                funcs = re.findall(r"func\s+(\w+)\s*\(", content)
                if funcs:
                    self.blueprint["go_routes"].append({f.stem: funcs})

    def generate_markdown(self):
        md = []
        md.append(f"# REPO BLUEPRINT: {self.blueprint['name']}")
        md.append(f"\n## 🛠 TECH STACK: {', '.join(self.blueprint['tech_stack'])}")
        
        if self.blueprint["django_apps"]:
            md.append("\n### 🏗 DATA MODELS (Django L2)")
            for model_path, fields in self.blueprint["models"].items():
                md.append(f"- **{model_path}**: `[{', '.join(fields)}]`")
            if self.blueprint["relationships"]:
                md.append("\n### 🔗 MODEL RELATIONSHIPS (L3)")
                for rel in sorted(list(set(self.blueprint["relationships"])))[:15]:
                    md.append(f"- {rel}")

        if self.blueprint["go_routes"]:
            md.append("\n### 🛣 GO ROUTES (L2)")
            for route_map in self.blueprint["go_routes"]:
                for file_name, funcs in route_map.items():
                    md.append(f"- **{file_name}.go**: `[{', '.join(funcs[:5])}]`")

        if self.blueprint["api_calls"]:
            md.append("\n### 🌐 API CONSUMPTION (L3 - Vue/TS)")
            # Sort by filename
            sorted_calls = sorted(self.blueprint["api_calls"], key=lambda x: list(x.keys())[0])
            for call_map in sorted_calls[:20]:
                for file_name, data in call_map.items():
                    info = []
                    if "urls" in data: info.append(f"urls: `[{', '.join(data['urls'])}]`")
                    if "imports" in data: info.append(f"imports: `[{', '.join(data['imports'])}]`")
                    md.append(f"- **{file_name}** -> {' | '.join(info)}")

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
