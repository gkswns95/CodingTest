"""
Configuration module for Notion-GitHub sync pipeline.
Loads environment variables from .env file.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# Notion API Configuration
NOTION_TOKEN = os.getenv('NOTION_TOKEN')
NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID')

# GitHub Configuration
GITHUB_REPO = os.getenv('GITHUB_REPO')

# Output Directory
OUTPUT_DIR = Path(os.getenv('OUTPUT_DIR', Path(__file__).parent.parent))

# Validate required environment variables
def validate_config():
    """Validate that all required environment variables are set."""
    missing = []
    if not NOTION_TOKEN:
        missing.append('NOTION_TOKEN')
    if not NOTION_DATABASE_ID:
        missing.append('NOTION_DATABASE_ID')
    
    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
    
    return True
