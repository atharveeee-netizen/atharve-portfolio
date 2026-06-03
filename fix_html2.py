import os

dir_path = '.'
for filename in os.listdir(dir_path):
    if filename.endswith('.html'):
        filepath = os.path.join(dir_path, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        orig_content = content
        
        # Fix the misplaced </body></html> tag
        content = content.replace('</body></html<main', '<main')
        content = content.replace('</body></html><main', '<main')
        
        # Fix howler.js script tag
        content = content.replace('<script defer="" src="js/howler.min.js"></script>', '<script defer="" type="module" src="js/howler.min.js"></script>')
        content = content.replace('<script src="js/howler.min.js"></script>', '<script type="module" src="js/howler.min.js"></script>')
        
        if content != orig_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'Fixed {filename}')
