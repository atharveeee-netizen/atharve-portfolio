import os
import re

def fix_html_files(directory):
    html_files = [f for f in os.listdir(directory) if f.endswith('.html')]
    for file_name in html_files:
        file_path = os.path.join(directory, file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Regex to remove integrity="..." and crossorigin="..."
        new_content = re.sub(r'\s+integrity="[^"]+"', '', content)
        new_content = re.sub(r'\s+crossorigin="[^"]+"', '', new_content)
        
        # Also remove type="module" warnings by changing text/javascript to module
        # Wait, the vite warning was: "can't be bundled without type="module" attribute"
        # We can change type="text/javascript" to type="module" for the pieter-koopt-demo JS files just in case.
        new_content = re.sub(
            r'type="text/javascript"\s*(?=.*js/pieter-koopt-demo)',
            'type="module" ',
            new_content
        )
        # Handle cases where src comes first
        new_content = re.sub(
            r'src="js/pieter-koopt-demo([^"]+)"\s+type="text/javascript"',
            r'src="js/pieter-koopt-demo\1" type="module"',
            new_content
        )
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Fixed {file_name}")

if __name__ == '__main__':
    fix_html_files('.')
