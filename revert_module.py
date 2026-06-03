import os

def revert_modules(directory):
    html_files = [f for f in os.listdir(directory) if f.endswith('.html')]
    for file_name in html_files:
        file_path = os.path.join(directory, file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace all type="module" with type="text/javascript"
        # Be careful about `<script type="module" src="...">`
        new_content = content.replace('type="module"', 'type="text/javascript"')
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Reverted {file_name}")

if __name__ == '__main__':
    revert_modules('.')
