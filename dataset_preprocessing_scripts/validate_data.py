"""
validate_data.py
Validates and cleans generated command data.
"""

import json
import re
import os
from pathlib import Path

# Known Windows CMD commands (NOT PowerShell)
VALID_CMD_COMMANDS = {
    'dir', 'cd', 'copy', 'move', 'del', 'rd', 'rmdir', 'md', 'mkdir',
    'type', 'echo', 'set', 'setx', 'find', 'findstr', 'sort', 'more',
    'ping', 'ipconfig', 'netstat', 'nslookup', 'tracert', 'curl',
    'certutil', 'attrib', 'icacls', 'fc', 'comp', 'xcopy', 'robocopy',
    'tasklist', 'taskkill', 'systeminfo', 'hostname', 'ver', 'date',
    'time', 'choco', 'winget', 'tar', 'where', 'start', 'call', 'if',
    'for', 'goto', 'rem', 'cls', 'title', 'color', 'pause', 'exit',
    'mklink', 'ren', 'rename', 'tree', 'assoc', 'ftype', 'path',
    'pushd', 'popd', 'subst', 'vol', 'label', 'format', 'chkdsk',
    'sfc', 'dism', 'wmic', 'reg', 'sc', 'net', 'shutdown', 'runas'
}

# PowerShell cmdlets to reject
POWERSHELL_PATTERNS = [
    r'Get-\w+', r'Set-\w+', r'Remove-\w+', r'New-\w+', r'Add-\w+',
    r'Clear-\w+', r'Copy-\w+', r'Move-\w+', r'Rename-\w+', r'Test-\w+',
    r'Write-\w+', r'Read-\w+', r'Out-\w+', r'ConvertTo-\w+', r'Import-\w+',
    r'Export-\w+', r'Invoke-\w+', r'Start-\w+', r'Stop-\w+', r'Select-\w+',
    r'Where-Object', r'ForEach-Object', r'\$_', r'\$\w+\s*=', r'-eq\s',
    r'-ne\s', r'-gt\s', r'-lt\s', r'-like\s', r'-match\s', r'\|%\{',
]

def is_powershell_command(cmd: str) -> bool:
    """Check if command looks like PowerShell instead of CMD."""
    for pattern in POWERSHELL_PATTERNS:
        if re.search(pattern, cmd, re.IGNORECASE):
            return True
    return False

def validate_windows_cmd(cmd: str) -> dict:
    """Validate Windows CMD command."""
    result = {"valid": True, "warnings": [], "errors": []}
    
    # Check for PowerShell
    if is_powershell_command(cmd):
        result["valid"] = False
        result["errors"].append("Contains PowerShell syntax, not CMD")
        return result
    
    # Check if starts with known CMD command
    first_word = cmd.split()[0].lower() if cmd.split() else ""
    # Remove any path prefix
    first_word = first_word.split('\\')[-1].split('/')[-1]
    
    if first_word not in VALID_CMD_COMMANDS and not first_word.endswith('.exe'):
        result["warnings"].append(f"Unknown CMD command: {first_word}")
    
    return result

def validate_linux_command(cmd: str) -> dict:
    """Basic validation for Linux command."""
    result = {"valid": True, "warnings": [], "errors": []}
    
    if not cmd.strip():
        result["valid"] = False
        result["errors"].append("Empty command")
    
    return result

def validate_entry(entry: dict) -> dict:
    """Validate a single data entry."""
    issues = {
        "id": entry.get("id", "unknown"),
        "valid": True,
        "errors": [],
        "warnings": []
    }
    
    # Required fields
    required = ["instruction", "linux", "windows_cmd", "mac"]
    for field in required:
        if field not in entry or not entry[field]:
            issues["valid"] = False
            issues["errors"].append(f"Missing required field: {field}")
    
    if not issues["valid"]:
        return issues
    
    # Validate Windows CMD
    cmd_result = validate_windows_cmd(entry["windows_cmd"])
    if not cmd_result["valid"]:
        issues["valid"] = False
        issues["errors"].extend(cmd_result["errors"])
    issues["warnings"].extend(cmd_result["warnings"])
    
    # Validate Linux
    linux_result = validate_linux_command(entry["linux"])
    if not linux_result["valid"]:
        issues["valid"] = False
        issues["errors"].extend(linux_result["errors"])
    
    # Check instruction quality
    if len(entry["instruction"]) < 10:
        issues["warnings"].append("Instruction too short")
    
    return issues

def validate_category_file(filepath: str) -> dict:
    """Validate an entire category file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    results = {
        "total": len(data),
        "valid": 0,
        "invalid": 0,
        "entries_with_warnings": 0,
        "issues": []
    }
    
    valid_entries = []
    
    for entry in data:
        validation = validate_entry(entry)
        
        if validation["valid"]:
            results["valid"] += 1
            valid_entries.append(entry)
            if validation["warnings"]:
                results["entries_with_warnings"] += 1
        else:
            results["invalid"] += 1
            results["issues"].append(validation)
    
    return results, valid_entries

def main():
    # Adjusted paths to match the user's workspace structure if needed
    # Assuming the script runs from Module1_dataset root
    raw_dir = Path("datasets/generated/raw")
    validated_dir = Path("datasets/generated/validated")
    validated_dir.mkdir(parents=True, exist_ok=True)
    
    if not raw_dir.exists():
        print(f"Directory not found: {raw_dir}")
        return

    for filepath in raw_dir.glob("*.json"):
        print(f"\nValidating: {filepath.name}")
        results, valid_entries = validate_category_file(filepath)
        
        print(f"  Total: {results['total']}")
        print(f"  Valid: {results['valid']}")
        print(f"  Invalid: {results['invalid']}")
        print(f"  With warnings: {results['entries_with_warnings']}")
        
        # Save valid entries
        output_path = validated_dir / filepath.name
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(valid_entries, f, indent=2, ensure_ascii=False)
        
        # Save issues report
        if results["issues"]:
            issues_path = validated_dir / f"{filepath.stem}_issues.json"
            with open(issues_path, 'w', encoding='utf-8') as f:
                json.dump(results["issues"], f, indent=2)
            print(f"  Issues saved to: {issues_path}")

if __name__ == "__main__":
    main()
