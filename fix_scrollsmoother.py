import os
import re

def fix_scrollsmoother(directory):
    html_files = [f for f in os.listdir(directory) if f.endswith('.html')]
    
    # Regex to match the script creation and onload wrapper
    # We want to replace:
    # const script = document.createElement('script');
    # script.src = '...';
    # script.onload = () => {
    #   <inner_code>
    # };
    # document.head.appendChild(script);
    # WITH: <inner_code>
    
    pattern = re.compile(
        r"const\s+script\s*=\s*document\.createElement\('script'\);\s*"
        r"script\.src\s*=\s*'https://cdn\.jsdelivr\.net/gh/devuncommon/gsap/ScrollSmoother\.min\.js';\s*"
        r"script\.onload\s*=\s*\(\)\s*=>\s*\{\s*"
        r"(.*?)"
        r"\s*\};\s*"
        r"document\.(?:head|body)\.appendChild\(script\);",
        re.DOTALL
    )

    for file_name in html_files:
        file_path = os.path.join(directory, file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content, count = pattern.subn(r'\1', content)
        
        if count > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Fixed {count} instances in {file_name}")

if __name__ == '__main__':
    fix_scrollsmoother('.')
