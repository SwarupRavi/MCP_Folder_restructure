"""Standalone file analyzer without MCP dependencies."""
import os
import time
from pathlib import Path
from datetime import datetime
from typing import Optional
from collections import defaultdict


def find_rarely_used_files(
    directory: str,
    days_threshold: int = 90,
    min_size_kb: Optional[int] = None,
    max_results: int = 100
) -> dict:
    """Find rarely used files based on last access time."""
    try:
        target_path = Path(directory).expanduser().resolve()
        if not target_path.exists():
            return {"error": f"Directory does not exist: {directory}"}
        
        if not target_path.is_dir():
            return {"error": f"Path is not a directory: {directory}"}
        
        threshold_time = time.time() - (days_threshold * 24 * 60 * 60)
        rarely_used = []
        total_size = 0
        
        for root, dirs, files in os.walk(target_path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                if file.startswith('.'):
                    continue
                    
                file_path = Path(root) / file
                try:
                    stat = file_path.stat()
                    access_time = stat.st_atime
                    size_kb = stat.st_size / 1024
                    
                    if min_size_kb and size_kb < min_size_kb:
                        continue
                    
                    if access_time < threshold_time:
                        days_since_access = (time.time() - access_time) / (24 * 60 * 60)
                        rarely_used.append({
                            "path": str(file_path.relative_to(target_path)),
                            "full_path": str(file_path),
                            "last_accessed": datetime.fromtimestamp(access_time).isoformat(),
                            "days_since_access": int(days_since_access),
                            "size_kb": round(size_kb, 2),
                            "size_mb": round(size_kb / 1024, 2)
                        })
                        total_size += size_kb
                        
                except (OSError, PermissionError):
                    continue
        
        rarely_used.sort(key=lambda x: x["days_since_access"], reverse=True)
        
        return {
            "directory": str(target_path),
            "threshold_days": days_threshold,
            "total_rarely_used": len(rarely_used),
            "total_size_mb": round(total_size / 1024, 2),
            "files": rarely_used[:max_results]
        }
        
    except Exception as e:
        return {"error": str(e)}


def get_file_stats(directory: str) -> dict:
    """Get overall statistics about files in a directory."""
    try:
        target_path = Path(directory).expanduser().resolve()
        if not target_path.exists():
            return {"error": f"Directory does not exist: {directory}"}
        
        now = time.time()
        stats = {
            "total_files": 0,
            "total_size_mb": 0,
            "accessed_last_30_days": 0,
            "accessed_last_90_days": 0,
            "accessed_last_year": 0,
            "older_than_year": 0
        }
        
        for root, dirs, files in os.walk(target_path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                if file.startswith('.'):
                    continue
                    
                file_path = Path(root) / file
                try:
                    stat = file_path.stat()
                    stats["total_files"] += 1
                    stats["total_size_mb"] += stat.st_size / (1024 * 1024)
                    
                    days_since_access = (now - stat.st_atime) / (24 * 60 * 60)
                    
                    if days_since_access <= 30:
                        stats["accessed_last_30_days"] += 1
                    elif days_since_access <= 90:
                        stats["accessed_last_90_days"] += 1
                    elif days_since_access <= 365:
                        stats["accessed_last_year"] += 1
                    else:
                        stats["older_than_year"] += 1
                        
                except (OSError, PermissionError):
                    continue
        
        stats["total_size_mb"] = round(stats["total_size_mb"], 2)
        return stats
        
    except Exception as e:
        return {"error": str(e)}


def find_duplicates(directory: str, min_size_kb: int = 0) -> dict:
    """Find duplicate files based on size and name."""
    try:
        target_path = Path(directory).expanduser().resolve()
        if not target_path.exists():
            return {"error": f"Directory does not exist: {directory}"}
        
        files_by_name_size = defaultdict(list)
        
        for root, dirs, files in os.walk(target_path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                if file.startswith('.'):
                    continue
                    
                file_path = Path(root) / file
                try:
                    stat = file_path.stat()
                    size_kb = stat.st_size / 1024
                    
                    if size_kb >= min_size_kb:
                        key = (file, stat.st_size)
                        files_by_name_size[key].append({
                            "path": str(file_path.relative_to(target_path)),
                            "full_path": str(file_path),
                            "size_kb": round(size_kb, 2),
                            "size_mb": round(size_kb / 1024, 2),
                            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                        })
                        
                except (OSError, PermissionError):
                    continue
        
        duplicates = []
        total_wasted_space = 0
        
        for (name, size), file_list in files_by_name_size.items():
            if len(file_list) > 1:
                size_kb = size / 1024
                wasted = size_kb * (len(file_list) - 1)
                total_wasted_space += wasted
                
                duplicates.append({
                    "filename": name,
                    "count": len(file_list),
                    "size_kb": round(size_kb, 2),
                    "size_mb": round(size_kb / 1024, 2),
                    "wasted_space_mb": round(wasted / 1024, 2),
                    "locations": file_list
                })
        
        duplicates.sort(key=lambda x: x["wasted_space_mb"], reverse=True)
        
        return {
            "directory": str(target_path),
            "total_duplicate_groups": len(duplicates),
            "total_wasted_space_mb": round(total_wasted_space / 1024, 2),
            "duplicates": duplicates
        }
        
    except Exception as e:
        return {"error": str(e)}


def find_large_files(directory: str, min_size_mb: int = 10, max_results: int = 50) -> dict:
    """Find the largest files in a directory."""
    try:
        target_path = Path(directory).expanduser().resolve()
        if not target_path.exists():
            return {"error": f"Directory does not exist: {directory}"}
        
        large_files = []
        total_size = 0
        
        for root, dirs, files in os.walk(target_path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                if file.startswith('.'):
                    continue
                    
                file_path = Path(root) / file
                try:
                    stat = file_path.stat()
                    size_mb = stat.st_size / (1024 * 1024)
                    
                    if size_mb >= min_size_mb:
                        large_files.append({
                            "filename": file,
                            "path": str(file_path.relative_to(target_path)),
                            "full_path": str(file_path),
                            "size_mb": round(size_mb, 2),
                            "size_gb": round(size_mb / 1024, 2),
                            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                            "accessed": datetime.fromtimestamp(stat.st_atime).isoformat()
                        })
                        total_size += size_mb
                        
                except (OSError, PermissionError):
                    continue
        
        large_files.sort(key=lambda x: x["size_mb"], reverse=True)
        
        return {
            "directory": str(target_path),
            "total_large_files": len(large_files),
            "total_size_gb": round(total_size / 1024, 2),
            "files": large_files[:max_results]
        }
        
    except Exception as e:
        return {"error": str(e)}


def analyze_by_extension(directory: str, top_n: int = 20) -> dict:
    """Analyze files grouped by extension."""
    try:
        target_path = Path(directory).expanduser().resolve()
        if not target_path.exists():
            return {"error": f"Directory does not exist: {directory}"}
        
        ext_stats = defaultdict(lambda: {"count": 0, "total_size_mb": 0})
        
        for root, dirs, files in os.walk(target_path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                if file.startswith('.'):
                    continue
                    
                file_path = Path(root) / file
                try:
                    stat = file_path.stat()
                    ext = file_path.suffix.lower() or "(no extension)"
                    
                    ext_stats[ext]["count"] += 1
                    ext_stats[ext]["total_size_mb"] += stat.st_size / (1024 * 1024)
                    
                except (OSError, PermissionError):
                    continue
        
        extensions = []
        for ext, stats in ext_stats.items():
            extensions.append({
                "extension": ext,
                "count": stats["count"],
                "total_size_mb": round(stats["total_size_mb"], 2),
                "total_size_gb": round(stats["total_size_mb"] / 1024, 2),
                "avg_size_mb": round(stats["total_size_mb"] / stats["count"], 2)
            })
        
        extensions.sort(key=lambda x: x["total_size_mb"], reverse=True)
        
        return {
            "directory": str(target_path),
            "total_extensions": len(extensions),
            "extensions": extensions[:top_n]
        }
        
    except Exception as e:
        return {"error": str(e)}


def suggest_cleanup(directory: str, days_threshold: int = 180, min_size_mb: int = 1) -> dict:
    """Suggest files for cleanup based on age and size."""
    try:
        target_path = Path(directory).expanduser().resolve()
        if not target_path.exists():
            return {"error": f"Directory does not exist: {directory}"}
        
        threshold_time = time.time() - (days_threshold * 24 * 60 * 60)
        suggestions = []
        total_space = 0
        
        for root, dirs, files in os.walk(target_path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                if file.startswith('.'):
                    continue
                    
                file_path = Path(root) / file
                try:
                    stat = file_path.stat()
                    size_mb = stat.st_size / (1024 * 1024)
                    
                    if stat.st_atime < threshold_time and size_mb >= min_size_mb:
                        days_since_access = (time.time() - stat.st_atime) / (24 * 60 * 60)
                        suggestions.append({
                            "path": str(file_path.relative_to(target_path)),
                            "full_path": str(file_path),
                            "size_mb": round(size_mb, 2),
                            "days_since_access": int(days_since_access),
                            "last_accessed": datetime.fromtimestamp(stat.st_atime).isoformat(),
                            "reason": f"Not accessed for {int(days_since_access)} days and {round(size_mb, 1)}MB"
                        })
                        total_space += size_mb
                        
                except (OSError, PermissionError):
                    continue
        
        suggestions.sort(key=lambda x: x["size_mb"], reverse=True)
        
        return {
            "directory": str(target_path),
            "criteria": f"Not accessed in {days_threshold} days and larger than {min_size_mb}MB",
            "total_suggestions": len(suggestions),
            "potential_space_savings_gb": round(total_space / 1024, 2),
            "suggestions": suggestions[:100]
        }
        
    except Exception as e:
        return {"error": str(e)}
