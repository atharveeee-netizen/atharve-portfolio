import os
import glob
import re

directory = r"C:\Users\noobg\.gemini\antigravity\scratch\atharve-portfolio"

css_to_inject = """<style id="navbar-pieterkoopt-clone">
  /* 1. Unify the Navigation Bar */
  .navbar {
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    background-color: #1a1a1a !important; /* Dark solid background */
    border-radius: 4px !important;
  }

  /* 2. Add Vertical Dividers to Left Column Items */
  .navbar_col.is-left > * {
    border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
  }
  
  /* 3. The Request Offer Compartment on the Right */
  .navbar_col.is-right {
    border-left: 1px solid rgba(255, 255, 255, 0.1) !important;
    padding-right: 0 !important;
    display: flex !important;
    align-items: center !important;
  }
  
  .navbar-cta {
    width: 100% !important;
    height: 100% !important;
    padding: 6px !important; /* Uniform padding so the green button fits snugly */
    display: flex !important;
    align-items: stretch !important;
  }
  
  /* 4. The Green Button inside the compartment */
  .navbar-cta > a.btn-animate-chars {
    width: 100% !important;
    height: 100% !important;
    border-radius: 4px !important;
    display: flex !important;
    align-items: center !important;
    margin: 0 !important;
  }
</style>
</head>"""

for filepath in glob.glob(os.path.join(directory, "*.html")):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 1. Remove the old pill override if it exists
    content = re.sub(r'<style id="navbar-cta-pill-override">.*?</style>\s*', '', content, flags=re.DOTALL)
    
    # 2. Remove the new clone css if it exists (so we don't duplicate it if run twice)
    content = re.sub(r'<style id="navbar-pieterkoopt-clone">.*?</style>\s*', '', content, flags=re.DOTALL)
    
    # 3. Inject the new clone css before </head>
    content = content.replace("</head>", css_to_inject)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Processed {filepath}")
