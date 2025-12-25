import os
import re

def clean_structure_text(structure_text: str):
    """Clean AI-generated structure text by removing comments and descriptions"""
    lines = structure_text.splitlines()
    cleaned_lines = []
    
    for line in lines:
        # Remove HTML entities
        line = line.replace('&lt;', '<').replace('&gt;', '>')
        
        # Remove comments (everything after <--, //, #)
        line = re.sub(r'\s*(<--|//|#).*$', '', line)
        
        # Remove extra descriptions in parentheses or quotes
        line = re.sub(r'\s*["\(].*?["\)]\s*$', '', line)
        
        # Clean but keep if not empty
        if line.strip():
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

def count_structure_items(structure_text: str):
    """Count folders and files in structure"""
    lines = structure_text.splitlines()
    folders = 0
    files = 0
    
    for line in lines:
        # Clean tree characters
        clean_line = (
            line.replace("├──", "")
            .replace("└──", "")
            .replace("│", "")
            .replace("─", "")
            .strip()
        )
        
        if clean_line:
            if clean_line.endswith('/'):
                folders += 1
            else:
                files += 1
    
    return folders, files

def build_structure(base_path: str, structure_text: str):
    """
    Build folder/file structure with proper nesting
    """
    # Clean the structure text first
    structure_text = clean_structure_text(structure_text)
    lines = structure_text.splitlines()
    
    if not lines:
        return []
    
    created_items = []
    path_stack = []
    
    for line in lines:
        # Count indentation level
        original_line = line
        depth = 0
        
        # Count tree characters to determine depth
        for char in line:
            if char in '│├└─ ':
                if char == '│':
                    depth += 1
                elif char in '├└':
                    depth += 1
                    break
            else:
                break
        
        # Clean the line
        clean_line = (
            line.replace("├──", "")
            .replace("└──", "")
            .replace("│", "")
            .replace("─", "")
            .strip()
        )
        
        if not clean_line:
            continue
        
        # Adjust path stack based on depth
        while len(path_stack) > depth:
            path_stack.pop()
        
        # Build current path
        if depth == 0:
            # Root level
            current_path = os.path.join(base_path, clean_line.rstrip('/'))
        else:
            # Nested level
            if path_stack:
                parent_path = os.path.join(base_path, *path_stack)
                current_path = os.path.join(parent_path, clean_line.rstrip('/'))
            else:
                current_path = os.path.join(base_path, clean_line.rstrip('/'))
        
        # Create folder or file
        if clean_line.endswith('/'):
            # It's a folder
            folder_name = clean_line.rstrip('/')
            os.makedirs(current_path, exist_ok=True)
            created_items.append(f"📁 {folder_name}")
            
            # Add to path stack for nested items
            if depth == 0:
                path_stack = [folder_name]
            else:
                path_stack = path_stack[:depth] + [folder_name]
        else:
            # It's a file
            os.makedirs(os.path.dirname(current_path), exist_ok=True)
            if not os.path.exists(current_path):
                with open(current_path, 'w', encoding='utf-8') as f:
                    f.write('')  # Create empty file
            created_items.append(f"📄 {clean_line}")
    
    return created_items


if __name__ == "__main__":
    # Example structure (tu apna structure paste kar sakta hai)
    test_structure = """MySoftware/
├── src/
│   ├── main.py
│   └── utils.py
├── config/
│   └── config.py
├── tests/
│   └── test_main.py
├── requirements.txt
├── setup.py
├── .gitignore
└── README.md
"""
    items = build_structure("D:/file testerer", test_structure)
    print(f"✅ Created {len(items)} items")
    for item in items:
        print(item)
