import glob

files = glob.glob('gemini-active/*.md')
target = chr(92) + 'n## LESSONS LEARNED (ANTI-PATTERNS)' + chr(92) + 'n'
replacement = chr(10) + chr(10) + '## LESSONS LEARNED (ANTI-PATTERNS)' + chr(10)

for f in files:
    with open(f, 'r') as file: 
        content = file.read()
    
    fixed_content = content.replace(target, replacement)
    
    with open(f, 'w') as file: 
        file.write(fixed_content)
    print(f"Fixed {f}")
