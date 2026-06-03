import os
from bs4 import BeautifulSoup, NavigableString

def extract_text(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    # Remove script, style, svg, path, noscript, meta, link
    for element in soup(['script', 'style', 'svg', 'path', 'noscript', 'meta', 'link', 'style']):
        element.decompose()
        
    def get_section(tag):
        # Go up the tree to find a section identifier
        parent = tag
        while parent:
            if parent.name in ['nav', 'header', 'footer', 'section', 'main']:
                class_names = parent.get('class', [])
                if class_names:
                    return f"{parent.name.capitalize()} ({' '.join(class_names)})"
                return parent.name.capitalize()
            if parent.get('class'):
                classes = parent.get('class')
                if isinstance(classes, list):
                    if any('hero' in c.lower() for c in classes):
                        return 'Hero'
                    if any('nav' in c.lower() for c in classes):
                        return 'Nav'
                    if any('footer' in c.lower() for c in classes):
                        return 'Footer'
            parent = parent.parent
        return 'Body'

    results = []
    
    # Process text nodes directly to avoid missing nested text
    for text_node in soup.find_all(string=True):
        text = text_node.strip()
        if not text:
            continue
            
        parent = text_node.parent
        if parent.name in ['script', 'style', 'head', 'html', 'body']:
            continue
            
        # Clean up text
        text = ' '.join(text.split())
        
        flag = ''
        if '{' in text or '}' in text or 'undefined' in text or 'null' in text or 'function(' in text:
            flag = ' ⚠️'
            
        section = get_section(parent)
        results.append(f"[Section: {section}] [Element: {parent.name}] — \"{text}\"{flag}")
        
    # Also process inputs and images for placeholders/alts
    for element in soup.find_all(['img', 'input', 'textarea']):
        text = ''
        if element.name == 'img' and element.get('alt'):
            text = f"[Alt Text] {element.get('alt')}"
        elif element.name in ['input', 'textarea'] and element.get('placeholder'):
            text = f"[Placeholder] {element.get('placeholder')}"
            
        if text:
            section = get_section(element)
            results.append(f"[Section: {section}] [Element: {element.name}] — \"{text}\"")

    # De-duplicate adjacent identical entries if any, though maybe just return as is
    return results

if __name__ == '__main__':
    results = extract_text('index.html')
    with open('extracted_text.txt', 'w', encoding='utf-8') as f:
        for r in results:
            f.write(r + '\n')
