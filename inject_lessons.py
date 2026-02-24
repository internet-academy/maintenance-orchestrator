import os
import glob

directory = 'gemini-active'
pattern = os.path.join(directory, '*.md')
files = glob.glob(pattern)

section_header = "
## LESSONS LEARNED (ANTI-PATTERNS)
"

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "## LESSONS LEARNED" not in content:
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(section_header)
        print(f"Injected into: {os.path.basename(file_path)}")
    else:
        print(f"Skipped (already exists): {os.path.basename(file_path)}")

print("Injection complete.")
