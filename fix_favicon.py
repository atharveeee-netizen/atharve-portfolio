import os
import glob

directory = r"C:\Users\noobg\.gemini\antigravity\scratch\atharve-portfolio"
old_icon_1 = "https://cdn.prod.website-files.com/67890d3b1a9365a1173c954e/6847f22fb31dc1494ed8bbb9_facicon.png"
old_icon_2 = "https://cdn.prod.website-files.com/67890d3b1a9365a1173c954e/6847f2715b26b743d3956e1b_Webckip.png"
new_icon = "assets/img/ashu-dither.png"

for filepath in glob.glob(os.path.join(directory, "*.html")):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    if old_icon_1 in content or old_icon_2 in content:
        content = content.replace(old_icon_1, new_icon)
        content = content.replace(old_icon_2, new_icon)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {filepath}")
