"""
Markdown exporter module.
Converts Notion blocks to Markdown and Python code files.
"""
import os
import re
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
from .config import OUTPUT_DIR


def sanitize_filename(name: str) -> str:
    """
    Sanitize a string to be used as a filename.
    
    Args:
        name: The original name.
        
    Returns:
        Sanitized filename.
    """
    # Remove or replace invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '', name)
    # Replace spaces with underscores
    sanitized = sanitized.replace(' ', '_')
    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip('. ')
    return sanitized


def blocks_to_markdown(blocks: List[Dict[str, Any]]) -> str:
    """
    Convert Notion blocks to Markdown format.
    
    Args:
        blocks: List of Notion block objects.
        
    Returns:
        Markdown string.
    """
    markdown_lines = []
    
    for block in blocks:
        block_type = block.get('type')
        
        if block_type == 'paragraph':
            text = extract_rich_text(block.get('paragraph', {}).get('rich_text', []))
            markdown_lines.append(text)
            markdown_lines.append('')
            
        elif block_type == 'heading_1':
            text = extract_rich_text(block.get('heading_1', {}).get('rich_text', []))
            markdown_lines.append(f'# {text}')
            markdown_lines.append('')
            
        elif block_type == 'heading_2':
            text = extract_rich_text(block.get('heading_2', {}).get('rich_text', []))
            markdown_lines.append(f'## {text}')
            markdown_lines.append('')
            
        elif block_type == 'heading_3':
            text = extract_rich_text(block.get('heading_3', {}).get('rich_text', []))
            markdown_lines.append(f'### {text}')
            markdown_lines.append('')
            
        elif block_type == 'bulleted_list_item':
            text = extract_rich_text(block.get('bulleted_list_item', {}).get('rich_text', []))
            markdown_lines.append(f'- {text}')
            
        elif block_type == 'numbered_list_item':
            text = extract_rich_text(block.get('numbered_list_item', {}).get('rich_text', []))
            markdown_lines.append(f'1. {text}')
            
        elif block_type == 'code':
            code_block = block.get('code', {})
            language = code_block.get('language', 'python')
            code_text = extract_rich_text(code_block.get('rich_text', []))
            markdown_lines.append(f'```{language}')
            markdown_lines.append(code_text)
            markdown_lines.append('```')
            markdown_lines.append('')
            
        elif block_type == 'quote':
            text = extract_rich_text(block.get('quote', {}).get('rich_text', []))
            markdown_lines.append(f'> {text}')
            markdown_lines.append('')
            
        elif block_type == 'divider':
            markdown_lines.append('---')
            markdown_lines.append('')
            
        elif block_type == 'callout':
            text = extract_rich_text(block.get('callout', {}).get('rich_text', []))
            emoji = block.get('callout', {}).get('icon', {}).get('emoji', '💡')
            markdown_lines.append(f'> {emoji} {text}')
            markdown_lines.append('')
            
        elif block_type == 'toggle':
            text = extract_rich_text(block.get('toggle', {}).get('rich_text', []))
            markdown_lines.append(f'<details><summary>{text}</summary>')
            markdown_lines.append('')
            markdown_lines.append('</details>')
            markdown_lines.append('')
    
    return '\n'.join(markdown_lines)


def extract_rich_text(rich_text_list: List[Dict[str, Any]]) -> str:
    """
    Extract plain text from Notion rich text array.
    
    Args:
        rich_text_list: List of rich text objects.
        
    Returns:
        Plain text string with basic formatting.
    """
    result = []
    
    for text_obj in rich_text_list:
        plain_text = text_obj.get('plain_text', '')
        annotations = text_obj.get('annotations', {})
        
        # Apply formatting
        if annotations.get('bold'):
            plain_text = f'**{plain_text}**'
        if annotations.get('italic'):
            plain_text = f'*{plain_text}*'
        if annotations.get('code'):
            plain_text = f'`{plain_text}`'
        if annotations.get('strikethrough'):
            plain_text = f'~~{plain_text}~~'
            
        result.append(plain_text)
    
    return ''.join(result)


def extract_code_blocks(blocks: List[Dict[str, Any]], language: str = 'python') -> List[str]:
    """
    Extract code blocks of a specific language from Notion blocks.
    
    Args:
        blocks: List of Notion block objects.
        language: Programming language to filter (default: python).
        
    Returns:
        List of code strings.
    """
    code_blocks = []
    
    for block in blocks:
        if block.get('type') == 'code':
            code_block = block.get('code', {})
            block_language = code_block.get('language', '').lower()
            
            if block_language == language.lower():
                code_text = extract_rich_text(code_block.get('rich_text', []))
                code_blocks.append(code_text)
    
    return code_blocks


def save_page_files(
    title: str,
    category: str,
    blocks: List[Dict[str, Any]],
    output_dir: Optional[Path] = None
) -> Tuple[Optional[str], Optional[str]]:
    """
    Save a page as Markdown file.
    
    Args:
        title: Page title (used for filename).
        category: Category/folder name (e.g., BFS, DFS).
        blocks: List of Notion block objects.
        output_dir: Base output directory (default: OUTPUT_DIR from config).
        
    Returns:
        Tuple of (markdown_path, None).
    """
    if output_dir is None:
        output_dir = OUTPUT_DIR
    
    if not title:
        return None, None
    
    # Determine folder path
    if category:
        folder_path = Path(output_dir) / sanitize_filename(category)
    else:
        folder_path = Path(output_dir) / 'Uncategorized'
    
    # Create folder if it doesn't exist
    folder_path.mkdir(parents=True, exist_ok=True)
    
    # Sanitize filename
    base_filename = sanitize_filename(title)
    
    # Generate Markdown content
    markdown_content = blocks_to_markdown(blocks)
    
    # Save Markdown file only
    md_path = folder_path / f'{base_filename}.md'
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(f'# {title}\n\n')
        f.write(markdown_content)
    
    return str(md_path), None

