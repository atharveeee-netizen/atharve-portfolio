import os

dir_path = '.'
for filename in os.listdir(dir_path):
    if filename.endswith('.html'):
        filepath = os.path.join(dir_path, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        orig_content = content
        
        # Fix the CSS syntax error
        content = content.replace('[data-gsap-text="false"] p,\n  opacity: 1 !important;', '[data-gsap-text="false"] p {\n  opacity: 1 !important;')
        content = content.replace('[data-gsap-text="false"] p,\r\n  opacity: 1 !important;', '[data-gsap-text="false"] p {\r\n  opacity: 1 !important;')
        
        # Fix unclosed cursor comment
        content = content.replace('</style></div><div class="cursor-selection-color w-embed"><style>', '</style>--></div><div class="cursor-selection-color w-embed"><style>')
        
        # Fix unclosed variable font comment
        content = content.replace('</style></div><div class="_w-button-override w-embed"><!-- Button Override -->', '</style>--></div><div class="_w-button-override w-embed"><!-- Button Override -->')
        
        # Fix Sound popup
        content = content.replace('<!-- Sound popup \n<script>', '<!-- Sound popup -->\n<script>')
        content = content.replace('<!-- Sound popup \r\n<script>', '<!-- Sound popup -->\r\n<script>')
        
        if content != orig_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'Fixed {filename}')
