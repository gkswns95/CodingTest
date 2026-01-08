"""
Git manager module.
Handles Git operations: commit and push to GitHub.
"""
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Tuple
from .config import OUTPUT_DIR, GITHUB_REPO


def run_git_command(args: List[str], cwd: Optional[Path] = None) -> Tuple[bool, str]:
    """
    Run a git command and return the result.
    
    Args:
        args: List of git command arguments.
        cwd: Working directory (default: OUTPUT_DIR).
        
    Returns:
        Tuple of (success, output/error message).
    """
    if cwd is None:
        cwd = OUTPUT_DIR
    
    try:
        result = subprocess.run(
            ['git'] + args,
            cwd=str(cwd),
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            return True, result.stdout.strip()
        else:
            return False, result.stderr.strip()
    except Exception as e:
        return False, str(e)


def is_git_repo(path: Optional[Path] = None) -> bool:
    """Check if the directory is a Git repository."""
    if path is None:
        path = OUTPUT_DIR
    
    git_dir = Path(path) / '.git'
    return git_dir.exists()


def init_repo() -> Tuple[bool, str]:
    """Initialize a new Git repository."""
    return run_git_command(['init'])


def add_remote(name: str = 'origin', url: Optional[str] = None) -> Tuple[bool, str]:
    """Add a remote to the repository."""
    if url is None:
        url = GITHUB_REPO
    
    # Check if remote already exists
    success, output = run_git_command(['remote', 'get-url', name])
    if success:
        # Remote exists, update it
        return run_git_command(['remote', 'set-url', name, url])
    else:
        # Remote doesn't exist, add it
        return run_git_command(['remote', 'add', name, url])


def get_changed_files() -> List[str]:
    """Get list of changed files (staged and unstaged)."""
    changed = []
    
    # Get unstaged changes
    success, output = run_git_command(['diff', '--name-only'])
    if success and output:
        changed.extend(output.split('\n'))
    
    # Get staged changes
    success, output = run_git_command(['diff', '--cached', '--name-only'])
    if success and output:
        changed.extend(output.split('\n'))
    
    # Get untracked files
    success, output = run_git_command(['ls-files', '--others', '--exclude-standard'])
    if success and output:
        changed.extend(output.split('\n'))
    
    return list(set(filter(None, changed)))


def stage_all() -> Tuple[bool, str]:
    """Stage all changes."""
    return run_git_command(['add', '-A'])


def commit(message: Optional[str] = None) -> Tuple[bool, str]:
    """
    Create a commit with the given message.
    
    Args:
        message: Commit message. If None, auto-generates one.
        
    Returns:
        Tuple of (success, output/error message).
    """
    if message is None:
        date_str = datetime.now().strftime('%Y-%m-%d %H:%M')
        changed_files = get_changed_files()
        
        if changed_files:
            # Get just filenames without extension for summary
            file_names = []
            for f in changed_files[:5]:  # Limit to 5 files
                name = Path(f).stem
                if name not in file_names:
                    file_names.append(name)
            
            files_summary = ', '.join(file_names[:3])
            if len(file_names) > 3:
                files_summary += f' 외 {len(file_names) - 3}개'
            
            message = f'[{date_str}] Sync: {files_summary}'
        else:
            message = f'[{date_str}] Sync update'
    
    return run_git_command(['commit', '-m', message])


def get_current_branch() -> str:
    """Get the current git branch name."""
    success, output = run_git_command(['rev-parse', '--abbrev-ref', 'HEAD'])
    if success and output:
        return output
    return 'master'  # Default fallback


def push(remote: str = 'origin', branch: str = None) -> Tuple[bool, str]:
    """
    Push commits to remote repository.
    
    Args:
        remote: Remote name (default: origin).
        branch: Branch name (default: auto-detect current branch).
        
    Returns:
        Tuple of (success, output/error message).
    """
    if branch is None:
        branch = get_current_branch()
    
    # Push to the current branch
    success, output = run_git_command(['push', '-u', remote, branch])
    
    return success, output


def setup_repo() -> Tuple[bool, str]:
    """
    Set up the Git repository if not already initialized.
    
    Returns:
        Tuple of (success, message).
    """
    messages = []
    
    # Check if already a git repo
    if not is_git_repo():
        success, msg = init_repo()
        if not success:
            return False, f'Failed to initialize repo: {msg}'
        messages.append('Initialized new Git repository')
    
    # Set up remote
    success, msg = add_remote()
    if success:
        messages.append(f'Remote set to: {GITHUB_REPO}')
    else:
        messages.append(f'Remote setup note: {msg}')
    
    return True, '\n'.join(messages)


def sync_to_github(commit_message: Optional[str] = None) -> Tuple[bool, str]:
    """
    Perform full sync: stage, commit, and push to GitHub.
    
    Args:
        commit_message: Optional custom commit message.
        
    Returns:
        Tuple of (success, summary message).
    """
    results = []
    
    # Ensure repo is set up
    success, msg = setup_repo()
    results.append(msg)
    
    # Check for changes
    changed_files = get_changed_files()
    if not changed_files:
        return True, 'No changes to sync.'
    
    results.append(f'Found {len(changed_files)} changed file(s)')
    
    # Stage all changes
    success, msg = stage_all()
    if not success:
        return False, f'Failed to stage changes: {msg}'
    results.append('Staged all changes')
    
    # Commit
    success, msg = commit(commit_message)
    if not success:
        if 'nothing to commit' in msg.lower():
            return True, 'Nothing to commit, working tree clean.'
        return False, f'Failed to commit: {msg}'
    results.append(f'Committed: {msg}')
    
    # Push
    success, msg = push()
    if not success:
        return False, f'Failed to push: {msg}'
    results.append('Pushed to GitHub')
    
    return True, '\n'.join(results)
