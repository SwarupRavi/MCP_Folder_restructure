#!/usr/bin/env python3
"""CLI wrapper for folder restructure MCP server."""
import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from folder_restructure_mcp.analyzer import (
    find_rarely_used_files,
    get_file_stats,
    find_duplicates,
    find_large_files,
    analyze_by_extension,
    suggest_cleanup
)

def print_json(data):
    """Pretty print JSON data."""
    print(json.dumps(data, indent=2))

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m folder_restructure_mcp.cli <command> [args]")
        print("\nCommands:")
        print("  rarely-used <directory> [days] [min_size_kb]")
        print("  stats <directory>")
        print("  duplicates <directory> [min_size_kb]")
        print("  large <directory> [min_size_mb] [max_results]")
        print("  extensions <directory> [top_n]")
        print("  cleanup <directory> [days] [min_size_mb]")
        print("\nExamples:")
        print("  python -m folder_restructure_mcp.cli large ~/Downloads 50")
        print("  python -m folder_restructure_mcp.cli duplicates ~/Downloads")
        print("  python -m folder_restructure_mcp.cli extensions ~/Projects")
        sys.exit(1)
    
    command = sys.argv[1]
    
    try:
        if command == "rarely-used":
            directory = sys.argv[2] if len(sys.argv) > 2 else "."
            days = int(sys.argv[3]) if len(sys.argv) > 3 else 90
            min_size = int(sys.argv[4]) if len(sys.argv) > 4 else None
            result = find_rarely_used_files(directory, days, min_size)
            print_json(result)
            
        elif command == "stats":
            directory = sys.argv[2] if len(sys.argv) > 2 else "."
            result = get_file_stats(directory)
            print_json(result)
            
        elif command == "duplicates":
            directory = sys.argv[2] if len(sys.argv) > 2 else "."
            min_size = int(sys.argv[3]) if len(sys.argv) > 3 else 0
            result = find_duplicates(directory, min_size)
            print_json(result)
            
        elif command == "large":
            directory = sys.argv[2] if len(sys.argv) > 2 else "."
            min_size = int(sys.argv[3]) if len(sys.argv) > 3 else 10
            max_results = int(sys.argv[4]) if len(sys.argv) > 4 else 50
            result = find_large_files(directory, min_size, max_results)
            print_json(result)
            
        elif command == "extensions":
            directory = sys.argv[2] if len(sys.argv) > 2 else "."
            top_n = int(sys.argv[3]) if len(sys.argv) > 3 else 20
            result = analyze_by_extension(directory, top_n)
            print_json(result)
            
        elif command == "cleanup":
            directory = sys.argv[2] if len(sys.argv) > 2 else "."
            days = int(sys.argv[3]) if len(sys.argv) > 3 else 180
            min_size = int(sys.argv[4]) if len(sys.argv) > 4 else 1
            result = suggest_cleanup(directory, days, min_size)
            print_json(result)
            
        else:
            print(f"Unknown command: {command}")
            sys.exit(1)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
