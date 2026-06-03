import os
import glob

directory = r"C:\Users\noobg\.gemini\antigravity\scratch\atharve-portfolio"

for filepath in glob.glob(os.path.join(directory, "*.html")):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Increase BG_TARGET
    content = content.replace("const BG_TARGET  = 0.10;", "const BG_TARGET  = 0.60;")
    
    # Increase fade target in intro
    content = content.replace("window.bgSound.fade(0, 0.10, 700);", "window.bgSound.fade(0, 0.60, 700);")
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Updated {filepath}")
