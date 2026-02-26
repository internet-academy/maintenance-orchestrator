import os
import json
import argparse
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

# Load API Key
BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class SemanticIndexer:
    def __init__(self, repo_path, output_file):
        self.repo_path = Path(repo_path).resolve()
        self.output_file = Path(output_file)
        self.cache_file = self.repo_path / ".gemini_semantics.json"
        self.semantics = self._load_cache()
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def _load_cache(self):
        if self.cache_file.exists():
            try:
                return json.loads(self.cache_file.read_text())
            except:
                return {}
        return {}

    def _save_cache(self):
        self.cache_file.write_text(json.dumps(self.semantics, indent=2))

    def get_summary(self, file_path):
        rel_path = str(file_path.relative_to(self.repo_path))
        if rel_path in self.semantics:
            return self.semantics[rel_path]

        print(f"🧠 Analyzing intent: {rel_path}...")
        try:
            content = file_path.read_text(errors='ignore')[:4000]
            prompt = f"File: {rel_path}\nSummarize the business logic intent of this file in 15 words or fewer.\n\nContent:\n{content}"
            response = self.model.generate_content(prompt)
            summary = response.text.strip().replace("\n", " ")
            self.semantics[rel_path] = summary
            return summary
        except Exception as e:
            return f"Error: {str(e)}"

    def run(self):
        target_files = []
        # DJANGO
        target_files.extend(list(self.repo_path.rglob("models.py")))
        target_files.extend(list(self.repo_path.rglob("views.py")))
        # GO
        target_files.extend(list(self.repo_path.rglob("backend/controllers/*.go")))
        # VUE
        target_files.extend(list(self.repo_path.rglob("frontend/src/views/*.vue")))

        md = ["# L4 SEMANTIC MAP\n"]
        for f in target_files:
            if "venv" in str(f) or "node_modules" in str(f): continue
            rel = str(f.relative_to(self.repo_path))
            summary = self.get_summary(f)
            md.append(f"- **{rel}**: {summary}")

        self._save_cache()
        self.output_file.write_text("\n".join(md))
        print(f"✅ L4 Semantic Map saved to {self.output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("output")
    args = parser.parse_args()
    SemanticIndexer(args.path, args.output).run()
