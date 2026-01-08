"""
Notion API client module.
Handles fetching pages and blocks from Notion database.
"""
from notion_client import Client
from typing import List, Dict, Any, Optional
from .config import NOTION_TOKEN, NOTION_DATABASE_ID, validate_config


def get_notion_client() -> Client:
    """Create and return a Notion client instance."""
    validate_config()
    return Client(auth=NOTION_TOKEN)


def get_child_pages(parent_page_id: str = None) -> List[Dict[str, Any]]:
    """
    Fetch all child pages from a parent page.
    
    Args:
        parent_page_id: Parent page ID. If None, uses NOTION_DATABASE_ID from config.
        
    Returns:
        List of child page objects.
    """
    client = get_notion_client()
    
    if parent_page_id is None:
        parent_page_id = NOTION_DATABASE_ID
    
    # Format ID with hyphens if needed
    if '-' not in parent_page_id and len(parent_page_id) == 32:
        parent_page_id = f'{parent_page_id[:8]}-{parent_page_id[8:12]}-{parent_page_id[12:16]}-{parent_page_id[16:20]}-{parent_page_id[20:]}'
    
    blocks = []
    has_more = True
    start_cursor = None
    
    while has_more:
        response = client.blocks.children.list(
            block_id=parent_page_id,
            start_cursor=start_cursor
        )
        blocks.extend(response.get('results', []))
        has_more = response.get('has_more', False)
        start_cursor = response.get('next_cursor')
    
    # Filter only child_page blocks
    child_pages = []
    for block in blocks:
        if block.get('type') == 'child_page':
            child_page_info = block.get('child_page', {})
            child_pages.append({
                'id': block.get('id'),
                'title': child_page_info.get('title', 'Untitled'),
                'type': 'child_page'
            })
    
    return child_pages


# Keep backward compatibility
def get_database_pages() -> List[Dict[str, Any]]:
    """Alias for get_child_pages for backward compatibility."""
    return get_child_pages()


def get_page_blocks(page_id: str) -> List[Dict[str, Any]]:
    """
    Fetch all blocks (content) from a specific page.
    
    Args:
        page_id: The ID of the page to fetch blocks from.
        
    Returns:
        List of block objects from the page.
    """
    client = get_notion_client()
    
    blocks = []
    has_more = True
    start_cursor = None
    
    while has_more:
        response = client.blocks.children.list(
            block_id=page_id,
            start_cursor=start_cursor
        )
        blocks.extend(response.get('results', []))
        has_more = response.get('has_more', False)
        start_cursor = response.get('next_cursor')
    
    return blocks


def get_page_property(page: Dict[str, Any], property_name: str) -> Optional[str]:
    """
    Extract a property value from a page object.
    
    Args:
        page: The page object.
        property_name: Name of the property to extract.
        
    Returns:
        The property value as a string, or None if not found.
    """
    properties = page.get('properties', {})
    prop = properties.get(property_name, {})
    prop_type = prop.get('type')
    
    if prop_type == 'title':
        title_list = prop.get('title', [])
        if title_list:
            return title_list[0].get('plain_text', '')
    elif prop_type == 'rich_text':
        text_list = prop.get('rich_text', [])
        if text_list:
            return text_list[0].get('plain_text', '')
    elif prop_type == 'select':
        select = prop.get('select')
        if select:
            return select.get('name', '')
    elif prop_type == 'multi_select':
        multi = prop.get('multi_select', [])
        return ', '.join([item.get('name', '') for item in multi])
    elif prop_type == 'number':
        return str(prop.get('number', ''))
    elif prop_type == 'url':
        return prop.get('url', '')
    
    return None


def extract_page_info(page: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract relevant information from a page object.
    
    Args:
        page: The page object.
        
    Returns:
        Dictionary with extracted page information.
    """
    properties = page.get('properties', {})
    
    # Try to find title property (could be named differently)
    title = None
    category = None
    
    for prop_name, prop_value in properties.items():
        prop_type = prop_value.get('type')
        
        if prop_type == 'title':
            title_list = prop_value.get('title', [])
            if title_list:
                title = ''.join([t.get('plain_text', '') for t in title_list])
        
        # Look for category/classification property
        if prop_type == 'select' and prop_name.lower() in ['분류', 'category', '자료구조', 'type', '유형']:
            select = prop_value.get('select')
            if select:
                category = select.get('name', '')
        
        if prop_type == 'multi_select' and prop_name.lower() in ['분류', 'category', '자료구조', 'type', '유형', '태그', 'tags']:
            multi = prop_value.get('multi_select', [])
            if multi:
                category = multi[0].get('name', '')  # Use first tag as category
    
    return {
        'id': page.get('id'),
        'title': title,
        'category': category,
        'url': page.get('url'),
        'last_edited': page.get('last_edited_time'),
        'properties': properties
    }
