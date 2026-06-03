import os
import glob

directory = r"C:\Users\noobg\.gemini\antigravity\scratch\atharve-portfolio"

for filepath in glob.glob(os.path.join(directory, "*.html")):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Fix the missing volume initialization on page load
    search_str = "  if (shouldPlaySound) {\n    bgSound.play();"
    replace_str = "  if (shouldPlaySound) {\n    bgSound.volume(v(BG_TARGET));\n    bgSound.play();"
    
    if search_str in content:
        content = content.replace(search_str, replace_str)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {filepath}")
    else:
        print(f"Skipped {filepath} (pattern not found)")
