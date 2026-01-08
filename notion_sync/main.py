#!/usr/bin/env python3
"""
Notion-GitHub Sync CLI.
Main entry point for syncing Notion content to GitHub.
"""
import sys
import argparse
from typing import Optional

from .config import validate_config, OUTPUT_DIR, NOTION_DATABASE_ID
from .notion_client import get_database_pages, get_page_blocks
from .markdown_exporter import save_page_files
from .git_manager import sync_to_github, setup_repo, get_changed_files


def pull_from_notion() -> bool:
    """
    Pull content from Notion and save as local files.
    Uses heading_2 blocks to determine category, dividers to separate sections.
    
    Returns:
        True if successful, False otherwise.
    """
    print('🔄 Fetching pages from Notion...')
    
    try:
        from notion_sync.notion_client import get_notion_client
        from notion_sync.config import NOTION_DATABASE_ID
        import re
        
        # Format database ID
        db_id = NOTION_DATABASE_ID
        if '-' not in db_id and len(db_id) == 32:
            db_id = f'{db_id[:8]}-{db_id[8:12]}-{db_id[12:16]}-{db_id[16:20]}-{db_id[20:]}'
        
        # Get all blocks from main page
        client = get_notion_client()
        blocks = []
        has_more = True
        start_cursor = None
        
        while has_more:
            response = client.blocks.children.list(
                block_id=db_id,
                start_cursor=start_cursor
            )
            blocks.extend(response.get('results', []))
            has_more = response.get('has_more', False)
            start_cursor = response.get('next_cursor')
        
        print(f'  Found {len(blocks)} blocks in main page')
        
        # Parse blocks to find categories and pages
        current_category = None
        pages_to_save = []
        
        for block in blocks:
            block_type = block.get('type')
            
            # Heading marks start of a new category
            if block_type in ('heading_1', 'heading_2', 'heading_3'):
                heading_data = block.get(block_type, {})
                rich_text = heading_data.get('rich_text', [])
                if rich_text:
                    heading_text = rich_text[0].get('plain_text', '')
                    # Extract category from heading (e.g., "DFS (Depth First Search)" -> "DFS")
                    if 'DFS' in heading_text.upper():
                        current_category = 'DFS'
                        print(f'  📁 Category: {heading_text} → DFS')
                    elif 'BFS' in heading_text.upper():
                        current_category = 'BFS'
                        print(f'  📁 Category: {heading_text} → BFS')
                    elif 'DP' in heading_text.upper():
                        current_category = 'DP'
                        print(f'  📁 Category: {heading_text} → DP')
                    else:
                        # Unknown category heading
                        category_match = re.match(r'^(\w+)', heading_text)
                        if category_match:
                            current_category = category_match.group(1)
                            print(f'  📁 Category: {heading_text} → {current_category}')
            
            # Divider optionally resets category (but we keep the current one)
            # since pages after divider but before next heading would be uncategorized
            
            # Child page - save with current category
            elif block_type == 'child_page':
                page_info = block.get('child_page', {})
                title = page_info.get('title', 'Untitled')
                page_id = block.get('id')
                
                if title and title != 'Untitled':
                    pages_to_save.append({
                        'id': page_id,
                        'title': title,
                        'category': current_category
                    })
        
        print(f'\n  Found {len(pages_to_save)} pages to save')
        
        # Save each page
        saved_count = 0
        for page in pages_to_save:
            title = page['title']
            page_id = page['id']
            category = page['category']
            
            print(f'  📄 {title} → {category or "Uncategorized"}')
            
            # Get page content
            blocks = get_page_blocks(page_id)
            
            # Save files
            md_path, _ = save_page_files(title, category, blocks)
            
            if md_path:
                print(f'     → {md_path}')
                saved_count += 1
        
        print(f'\n✅ Saved {saved_count} page(s) to local files')
        return True
        
    except Exception as e:
        print(f'\n❌ Error pulling from Notion: {e}')
        import traceback
        traceback.print_exc()
        return False


def push_to_github(message: Optional[str] = None) -> bool:
    """
    Push local changes to GitHub.
    
    Args:
        message: Optional commit message.
        
    Returns:
        True if successful, False otherwise.
    """
    print('🚀 Pushing to GitHub...')
    
    try:
        success, result = sync_to_github(message)
        
        if success:
            print(f'\n✅ {result}')
        else:
            print(f'\n❌ {result}')
        
        return success
        
    except Exception as e:
        print(f'\n❌ Error pushing to GitHub: {e}')
        return False


def full_sync(message: Optional[str] = None) -> bool:
    """
    Perform full sync: Notion → Local → GitHub.
    
    Args:
        message: Optional commit message.
        
    Returns:
        True if successful, False otherwise.
    """
    print('=' * 50)
    print('🔄 Starting full sync: Notion → Local → GitHub')
    print('=' * 50)
    print()
    
    # Step 1: Pull from Notion
    if not pull_from_notion():
        return False
    
    print()
    
    # Step 2: Push to GitHub
    if not push_to_github(message):
        return False
    
    print()
    print('=' * 50)
    print('✅ Full sync completed!')
    print('=' * 50)
    
    return True


def status() -> None:
    """Show current status."""
    print('📊 Current Status')
    print('=' * 50)
    print(f'  Output directory: {OUTPUT_DIR}')
    print(f'  Database ID: {NOTION_DATABASE_ID[:8]}...')
    
    changed = get_changed_files()
    if changed:
        print(f'\n  📝 Changed files ({len(changed)}):')
        for f in changed[:10]:
            print(f'     - {f}')
        if len(changed) > 10:
            print(f'     ... and {len(changed) - 10} more')
    else:
        print('\n  ✅ No uncommitted changes')


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Sync Notion coding test notes to GitHub',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python -m notion_sync sync           # Full sync: Notion → Local → GitHub
  python -m notion_sync pull           # Only pull from Notion to local
  python -m notion_sync push           # Only push local changes to GitHub
  python -m notion_sync status         # Show current status
        '''
    )
    
    parser.add_argument(
        'command',
        choices=['sync', 'pull', 'push', 'status'],
        help='Command to execute'
    )
    
    parser.add_argument(
        '-m', '--message',
        help='Custom commit message (for sync and push commands)'
    )
    
    args = parser.parse_args()
    
    # Validate configuration
    try:
        validate_config()
    except ValueError as e:
        print(f'❌ Configuration error: {e}')
        print('  Please check your .env file.')
        sys.exit(1)
    
    # Execute command
    if args.command == 'sync':
        success = full_sync(args.message)
    elif args.command == 'pull':
        success = pull_from_notion()
    elif args.command == 'push':
        success = push_to_github(args.message)
    elif args.command == 'status':
        status()
        success = True
    else:
        parser.print_help()
        success = False
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
