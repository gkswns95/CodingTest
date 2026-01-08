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
    
    Returns:
        True if successful, False otherwise.
    """
    print('🔄 Fetching pages from Notion...')
    
    try:
        # Get child pages from main page
        pages = get_database_pages()
        print(f'  Found {len(pages)} child page(s)')
        
        if not pages:
            print('  No child pages found.')
            return True
        
        saved_count = 0
        for page in pages:
            title = page.get('title', 'Untitled')
            page_id = page.get('id')
            
            if not title or title == 'Untitled':
                print(f'  ⚠️  Skipping page without title')
                continue
            
            print(f'  📄 Processing: {title}')
            
            # Get page content (blocks)
            blocks = get_page_blocks(page_id)
            
            # Extract category from title (e.g., "(DFS)" or "(BFS)")
            import re
            category = None
            category_match = re.search(r'\((DFS|BFS|DP|그래프|정렬|탐색|트리|힙|스택|큐|해시)\)', title, re.IGNORECASE)
            if category_match:
                category = category_match.group(1).upper()
            elif 'DFS' in title.upper():
                category = 'DFS'
            elif 'BFS' in title.upper():
                category = 'BFS'
            
            # Save files
            md_path, py_path = save_page_files(title, category, blocks)
            
            if md_path:
                print(f'     → Saved: {md_path}')
                saved_count += 1
            if py_path:
                print(f'     → Saved: {py_path}')
        
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
