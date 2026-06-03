import os
import glob
import re

directory = r"C:\Users\noobg\.gemini\antigravity\scratch\atharve-portfolio"

css_to_inject = """<style id="navbar-pieterkoopt-clone">
  /* 1. Unify the Navigation Bar */
  .navbar {
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    background-color: #1a1a1a !important;
    border-radius: 4px !important;
  }

  /* 2. Fix the Logo Compartment */
  .navbar_col.is-left > a.navbar_logo {
    margin-right: 0 !important;       /* Remove inline margin */
    padding-left: 1.5rem !important;  /* Make the compartment spacious */
    padding-right: 1.5rem !important;
  }

  /* 3. Add Vertical Dividers to Left Column Items */
  .navbar_col.is-left > * {
    border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
  }
  
  /* Remove any conflicting inline left-borders on the icons */
  .navbar_col.is-left > .navbar-item {
    border-left: none !important;
  }
  
  /* 4. Make the center column take up the remaining space */
  .navbar_col.is-center {
    flex-grow: 1 !important;
  }
  
  /* 5. The Request Offer Compartment on the Right */
  .navbar_col.is-right {
    flex: 0 0 auto !important; /* DO NOT stretch out */
    border-left: 1px solid rgba(255, 255, 255, 0.1) !important;
    padding-right: 0 !important;
    display: flex !important;
    align-items: stretch !important;
    height: 100% !important;
  }
  
  .navbar-cta {
    width: auto !important;
    height: 100% !important;
    padding: 6px !important; 
    display: flex !important;
    align-items: stretch !important;
  }
  
  /* 6. The Green Button inside the compartment */
  .navbar-cta > a.btn-animate-chars {
    width: auto !important;
    height: 100% !important;
    border-radius: 4px !important;
    display: flex !important;
    align-items: center !important;
    margin: 0 !important;
    padding-left: 1.5rem !important; 
    padding-right: 1.5rem !important;
  }
</style>
</head>"""

for filepath in glob.glob(os.path.join(directory, "*.html")):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace the existing clone style
    content = re.sub(r'<style id="navbar-pieterkoopt-clone">.*?</style>\s*</head>', css_to_inject, content, flags=re.DOTALL)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Fixed gap in {filepath}")
