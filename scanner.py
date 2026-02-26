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
            self._deep_parse_django_models()
        if (self.repo_path / "backend/go.mod").exists() or (self.repo_path / "go.mod").exists():
            self.blueprint["tech_stack"].append("Go")
            self._deep_parse_go_models()
        if (self.repo_path / "package.json").exists():
            self.blueprint["tech_stack"].append("Node.js/Frontend")

    def _deep_parse_django_models(self):
        # Find ALL models.py files
        for model_file in self.repo_path.rglob("models.py"):
            if "venv" in str(model_file) or "migrations" in str(model_file):
                continue
            
            app_name = model_file.parent.name
            try:
                tree = ast.parse(model_file.read_text())
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        model_name = node.name
                        fields = []
                        for subnode in ast.walk(node):
                            if isinstance(subnode, ast.Assign) and isinstance(subnode.value, ast.Call):
                                func_name = ""
                                if hasattr(subnode.value.func, 'attr'): func_name = subnode.value.func.attr
                                elif hasattr(subnode.value.func, 'id'): func_name = subnode.value.func.id
                                    
                                if func_name in ['ForeignKey', 'OneToOneField', 'ManyToManyField']:
                                    if subnode.value.args and isinstance(subnode.value.args[0], (ast.Constant, ast.Str)):
                                        target = subnode.value.args[0].s if hasattr(subnode.value.args[0], 's') else subnode.value.args[0].value
                                        self.blueprint["relationships"].append(f"{app_name}.{model_name} -> {target}")
                                
                                if isinstance(subnode.targets[0], ast.Name):
                                    fields.append(subnode.targets[0].id)
                        
                        if fields:
                            self.blueprint["models"][f"{app_name}.{model_name}"] = fields[:8]
            except Exception:
                pass

    def _deep_parse_go_models(self):
        # Find all .go files in models/ directories
        for model_file in self.repo_path.rglob("models/*.go"):
            try:
                content = model_file.read_text()
                structs = re.findall(r"type\s+(\w+)\s+struct\s+{(.*?)}", content, re.DOTALL)
                for struct_name, body in structs:
                    fields = re.findall(r"^\s+(\w+)\s+", body, re.MULTILINE)
                    if fields:
                        self.blueprint["models"][f"Go.{struct_name}"] = fields[:8]
            except Exception:
                pass
        
        # Also parse routes for route intelligence
        routes_dir = self.repo_path / "backend" / "routes"
        if not routes_dir.exists(): routes_dir = self.repo_path / "routes"
        if routes_dir.exists():
            for f in routes_dir.glob("*.go"):
                funcs = re.findall(r"func\s+(\w+)\s*\(", f.read_text())
                if funcs: self.blueprint["go_routes"].append({f.stem: funcs})

    def generate_markdown(self):
        md = []
        md.append(f"# REPO BLUEPRINT: {self.blueprint['name']}")
        md.append(f"\n## 🏗 DATA MODELS ({len(self.blueprint['models'])} discovered)")
        
        # Group models by app for readability
        for model_path, fields in sorted(self.blueprint["models"].items()):
            md.append(f"- **{model_path}**: `[{', '.join(fields)}]`")
        
        if self.blueprint["relationships"]:
            md.append("\n### 🔗 RELATIONSHIPS")
            for rel in sorted(list(set(self.blueprint["relationships"])))[:20]:
                md.append(f"- {rel}")

        if self.blueprint["go_routes"]:
            md.append("\n### 🛣 GO ROUTES")
            for route_map in self.blueprint["go_routes"]:
                for file_name, funcs in route_map.items():
                    md.append(f"- **{file_name}.go**: `[{', '.join(funcs[:3])}]`")

        md.append("\n## 📂 DIRECTORY STRUCTURE")
        md.append("```")
        md.extend(self.blueprint["structure"])
        md.append("```")
        return "\n".join(md)

    def run(self):
        print(f"🚀 Deep Scanning {self.repo_path}...")
        self.detect_tech_stack()
        self.scan(self.repo_path)
        output = self.generate_markdown()
        if self.output_file:
            with open(self.output_file, "w") as f:
                f.write(output)
            print(f"✅ Deep Blueprint saved to {self.output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--output")
    args = parser.parse_args()
    RepoScanner(args.path, args.output).run()
