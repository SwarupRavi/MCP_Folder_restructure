# Folder Restructure MCP Server

An MCP server that analyzes file access times to help identify rarely used files for folder restructuring.

## Features

- **find_rarely_used_files**: Find files that haven't been accessed in a specified number of days
- **get_file_stats**: Get overall statistics about file access patterns in a directory
- **find_duplicates**: Find duplicate files based on size and name, calculate wasted space
- **find_large_files**: Identify the largest files taking up space
- **analyze_by_extension**: Group files by type (.jpg, .mp4, etc.) showing count and total size
- **suggest_cleanup**: Smart cleanup suggestions based on age and size

## Installation

```bash
# Install uv (required)
brew install uv

# The server will be run via uvx, no additional installation needed
```

## Configuration

Already configured in `.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "folder-restructure": {
      "command": "uvx",
      "args": [
        "--directory",
        "/Users/swarupravi/Downloads/MCP_server_folder",
        "fastmcp",
        "run",
        "folder_restructure_mcp/server.py"
      ],
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

## How to Use

### Method 1: Through Kiro AI (Easiest)
Just ask me in natural language:

```
"Find duplicate files in ~/Downloads"
"Show me the largest files in ~/Documents over 50MB"
"What file types are taking up space in ~/Projects"
"Find files in ~/Downloads not accessed in 6 months"
"Suggest cleanup for ~/Downloads"
```

I'll automatically call the right MCP tools and show you the results!

### Method 2: Terminal CLI (Direct Access)
Use the `folder-analyze` command:

```bash
# Find large files over 100MB
./folder-analyze large ~/Downloads 100 10

# Find duplicates
./folder-analyze duplicates ~/Downloads

# Analyze by file extension
./folder-analyze extensions ~/Projects

# Get file access statistics
./folder-analyze stats ~/Documents

# Find rarely used files (not accessed in 180 days)
./folder-analyze rarely-used ~/Downloads 180

# Get cleanup suggestions
./folder-analyze cleanup ~/Downloads 180 5
```

**Available Commands:**
- `large <dir> [min_mb] [max_results]` - Find largest files
- `duplicates <dir> [min_kb]` - Find duplicate files
- `extensions <dir> [top_n]` - Analyze by file type
- `stats <dir>` - Get access statistics
- `rarely-used <dir> [days] [min_kb]` - Find old files
- `cleanup <dir> [days] [min_mb]` - Get cleanup suggestions

### Method 2: Direct Testing (Terminal)
Test the server directly:

```bash
# Run in development mode with interactive testing
uvx fastmcp dev folder_restructure_mcp/server.py

# Or run the server
uvx --directory /Users/swarupravi/Downloads/MCP_server_folder fastmcp run folder_restructure_mcp/server.py
```

### Method 3: Python Script
Create a test script:

```python
from folder_restructure_mcp.server import (
    find_rarely_used_files,
    find_duplicates,
    find_large_files,
    analyze_by_extension,
    suggest_cleanup
)

# Find large files
result = find_large_files("~/Downloads", min_size_mb=50, max_results=10)
print(result)

# Find duplicates
result = find_duplicates("~/Downloads", min_size_kb=100)
print(result)
```

## Tool Reference

### find_rarely_used_files
Find files not accessed recently.
- `directory`: Path to analyze (required)
- `days_threshold`: Days since last access (default: 90)
- `min_size_kb`: Minimum file size in KB (optional)
- `max_results`: Maximum results to return (default: 100)

### get_file_stats
Get overall file access statistics.
- `directory`: Path to analyze (required)

### find_duplicates
Find duplicate files and wasted space.
- `directory`: Path to analyze (required)
- `min_size_kb`: Only check files larger than this (default: 0)

### find_large_files
Find the largest files.
- `directory`: Path to analyze (required)
- `min_size_mb`: Minimum file size in MB (default: 10)
- `max_results`: Maximum results to return (default: 50)

### analyze_by_extension
Analyze files grouped by extension.
- `directory`: Path to analyze (required)
- `top_n`: Number of top extensions to return (default: 20)

### suggest_cleanup
Smart cleanup suggestions.
- `directory`: Path to analyze (required)
- `days_threshold`: Files not accessed in this many days (default: 180)
- `min_size_mb`: Minimum file size in MB (default: 1)

## Examples

Ask me any of these:

1. **"Find duplicates in ~/Downloads"**
   - Shows duplicate files and how much space you could save

2. **"What are my largest files in ~/Documents?"**
   - Lists files over 10MB sorted by size

3. **"Analyze file types in ~/Projects"**
   - Shows which extensions (.js, .py, .mp4) take up the most space

4. **"Suggest cleanup for ~/Downloads"**
   - Smart suggestions for old, large files you might want to delete

5. **"Find files in ~/Desktop not accessed in 1 year"**
   - Lists files you haven't touched in 365+ days

## Automated Analysis (Cron Job)

Run analysis automatically every 6 hours and save reports:

```bash
# Setup cron job (runs at 00:00, 06:00, 12:00, 18:00)
./setup-cron.sh

# Run analysis manually
./run-analysis.sh

# View reports
./view-reports.sh --latest

# Check cron job status
crontab -l

# Remove cron job
crontab -l | grep -v 'run-analysis.sh' | crontab -
```

**Reports Location:** `analysis-reports/analysis_YYYYMMDD_HHMMSS.json`

Each report includes:
- Large files (>50MB)
- Duplicate files (>100KB)
- File statistics
- File type analysis
- Cleanup suggestions

Reports are automatically cleaned up (keeps last 30).

## Development

Run locally for testing:
```bash
uvx fastmcp dev folder_restructure_mcp/server.py
```
