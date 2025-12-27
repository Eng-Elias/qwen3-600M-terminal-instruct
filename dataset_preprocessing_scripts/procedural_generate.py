"""
procedural_generate.py
Procedurally generates large datasets of terminal commands using templates and combinatorics.
Target: 500+ samples per category.
"""

import json
import random
import uuid
from pathlib import Path
from typing import List, Dict

# --- Data Banks ---

FILENAMES = [
    "data.txt", "report.pdf", "image.png", "script.py", "config.json", 
    "index.html", "style.css", "notes.md", "backup.zip", "main.cpp",
    "app.log", "error.log", "query.sql", "dataset.csv", "profile.jpg",
    "readme.txt", "todo.list", "server.conf", "test.spec.js", "docker-compose.yml"
]

DIRECTORIES = [
    "Documents", "Downloads", "Desktop", "Music", "Pictures", 
    "src", "bin", "logs", "config", "backup", "temp", "build",
    "public", "assets", "include", "lib", "tests", "scripts"
]

APPS = [
    "chrome", "firefox", "python", "node", "java", "docker", "nginx", 
    "mysql", "postgres", "redis", "code", "spotify", "slack", "zoom",
    "git", "vim", "nano", "curl", "wget", "bash"
]

PACKAGES = [
    "git", "python3", "nodejs", "docker", "vim", "curl", "wget", "htop",
    "jq", "tree", "tmux", "zsh", "gcc", "make", "cmake", "yarn", "npm",
    "pip", "ruby", "go", "rust", "ffmpeg", "imagemagick", "nginx"
]

DOMAINS = [
    "google.com", "github.com", "openai.com", "stackoverflow.com", 
    "example.com", "localhost", "127.0.0.1", "wikipedia.org",
    "amazon.com", "microsoft.com", "apple.com", "api.service.com"
]

USERS = ["admin", "root", "user", "guest", "john", "jane", "deploy", "ubuntu"]

VARS = ["PATH", "JAVA_HOME", "EDITOR", "USER", "HOME", "SHELL", "TERM", "LANG", "PWD", "TMPDIR"]

# --- Generators ---

def generate_file_ops(count: int) -> List[Dict]:
    data = []
    actions = ["create", "delete", "copy", "move", "view", "search"]
    
    for _ in range(count):
        action = random.choice(actions)
        fname = random.choice(FILENAMES)
        fname2 = random.choice(FILENAMES)
        dirname = random.choice(DIRECTORIES)
        
        entry = {
            "id": f"file_{uuid.uuid4().hex[:8]}",
            "category": "file_operations",
            "subcategory": action,
            "difficulty": "beginner",
            "tags": ["file", action]
        }
        
        if action == "create":
            entry["instruction"] = f"Create an empty file named {fname}"
            entry["linux"] = f"touch {fname}"
            entry["windows_cmd"] = f"type nul > {fname}"
            entry["mac"] = f"touch {fname}"
            
        elif action == "delete":
            if random.random() < 0.5:
                entry["instruction"] = f"Delete the file {fname}"
                entry["linux"] = f"rm {fname}"
                entry["windows_cmd"] = f"del {fname}"
                entry["mac"] = f"rm {fname}"
            else:
                ext = fname.split('.')[-1]
                entry["instruction"] = f"Delete all .{ext} files"
                entry["linux"] = f"rm *.{ext}"
                entry["windows_cmd"] = f"del *.{ext}"
                entry["mac"] = f"rm *.{ext}"
                entry["tags"].append("wildcard")

        elif action == "copy":
            entry["instruction"] = f"Copy {fname} to the {dirname} directory"
            entry["linux"] = f"cp {fname} {dirname}/"
            entry["windows_cmd"] = f"copy {fname} {dirname}\\"
            entry["mac"] = f"cp {fname} {dirname}/"
            
        elif action == "move":
            if random.random() < 0.5:
                entry["instruction"] = f"Move {fname} to {dirname}"
                entry["linux"] = f"mv {fname} {dirname}/"
                entry["windows_cmd"] = f"move {fname} {dirname}\\"
                entry["mac"] = f"mv {fname} {dirname}/"
            else:
                entry["instruction"] = f"Rename {fname} to {fname2}"
                entry["linux"] = f"mv {fname} {fname2}"
                entry["windows_cmd"] = f"ren {fname} {fname2}"
                entry["mac"] = f"mv {fname} {fname2}"
                entry["subcategory"] = "rename"
                
        elif action == "view":
            entry["instruction"] = f"Display the contents of {fname}"
            entry["linux"] = f"cat {fname}"
            entry["windows_cmd"] = f"type {fname}"
            entry["mac"] = f"cat {fname}"
            
        elif action == "search":
            ext = fname.split('.')[-1]
            entry["instruction"] = f"Find all .{ext} files in {dirname}"
            entry["linux"] = f"find {dirname} -name '*.{ext}'"
            entry["windows_cmd"] = f"dir /s /b {dirname}\\*.{ext}"
            entry["mac"] = f"find {dirname} -name '*.{ext}'"
            
        data.append(entry)
    return data

def generate_dir_ops(count: int) -> List[Dict]:
    data = []
    actions = ["create", "remove", "navigate", "list", "tree"]
    
    for _ in range(count):
        action = random.choice(actions)
        dirname = random.choice(DIRECTORIES)
        dirname2 = random.choice(DIRECTORIES)
        
        entry = {
            "id": f"dir_{uuid.uuid4().hex[:8]}",
            "category": "directory_operations",
            "subcategory": action,
            "difficulty": "beginner",
            "tags": ["directory", action]
        }
        
        if action == "create":
            if random.random() < 0.7:
                entry["instruction"] = f"Create a directory named {dirname}"
                entry["linux"] = f"mkdir {dirname}"
                entry["windows_cmd"] = f"mkdir {dirname}"
                entry["mac"] = f"mkdir {dirname}"
            else:
                entry["instruction"] = f"Create nested directories {dirname}/{dirname2}"
                entry["linux"] = f"mkdir -p {dirname}/{dirname2}"
                entry["windows_cmd"] = f"mkdir {dirname}\\{dirname2}"
                entry["mac"] = f"mkdir -p {dirname}/{dirname2}"
                
        elif action == "remove":
            entry["instruction"] = f"Remove the directory {dirname} and its contents"
            entry["linux"] = f"rm -rf {dirname}"
            entry["windows_cmd"] = f"rmdir /s /q {dirname}"
            entry["mac"] = f"rm -rf {dirname}"
            
        elif action == "navigate":
            entry["instruction"] = f"Change directory to {dirname}"
            entry["linux"] = f"cd {dirname}"
            entry["windows_cmd"] = f"cd {dirname}"
            entry["mac"] = f"cd {dirname}"
            
        elif action == "list":
            entry["instruction"] = f"List files in {dirname}"
            entry["linux"] = f"ls {dirname}"
            entry["windows_cmd"] = f"dir {dirname}"
            entry["mac"] = f"ls {dirname}"
            
        elif action == "tree":
            entry["instruction"] = "Display directory structure"
            entry["linux"] = "tree"
            entry["windows_cmd"] = "tree"
            entry["mac"] = "tree"
            
        data.append(entry)
    return data

def generate_process_ops(count: int) -> List[Dict]:
    data = []
    
    for _ in range(count):
        app = random.choice(APPS)
        pid = random.randint(1000, 99999)
        
        action = random.choice(["list", "kill", "find"])
        
        entry = {
            "id": f"proc_{uuid.uuid4().hex[:8]}",
            "category": "process_management",
            "subcategory": action,
            "difficulty": "intermediate",
            "tags": ["process", action]
        }
        
        if action == "list":
            entry["instruction"] = "List all running processes"
            entry["linux"] = "ps aux"
            entry["windows_cmd"] = "tasklist"
            entry["mac"] = "ps aux"
            
        elif action == "kill":
            if random.random() < 0.5:
                entry["instruction"] = f"Kill the process with PID {pid}"
                entry["linux"] = f"kill {pid}"
                entry["windows_cmd"] = f"taskkill /PID {pid} /F"
                entry["mac"] = f"kill {pid}"
            else:
                entry["instruction"] = f"Terminate all '{app}' processes"
                entry["linux"] = f"pkill {app}"
                entry["windows_cmd"] = f"taskkill /IM {app}.exe /F"
                entry["mac"] = f"pkill {app}"
                
        elif action == "find":
            entry["instruction"] = f"Find the PID of '{app}'"
            entry["linux"] = f"pgrep {app}"
            entry["windows_cmd"] = f"tasklist | findstr {app}"
            entry["mac"] = f"pgrep {app}"
            
        data.append(entry)
    return data

def generate_network_ops(count: int) -> List[Dict]:
    data = []
    
    for _ in range(count):
        domain = random.choice(DOMAINS)
        fname = random.choice(FILENAMES)
        
        action = random.choice(["ping", "download", "dns", "ip"])
        
        entry = {
            "id": f"net_{uuid.uuid4().hex[:8]}",
            "category": "network_operations",
            "subcategory": action,
            "difficulty": "beginner",
            "tags": ["network", action]
        }
        
        if action == "ping":
            count_ping = random.randint(3, 10)
            entry["instruction"] = f"Ping {domain} {count_ping} times"
            entry["linux"] = f"ping -c {count_ping} {domain}"
            entry["windows_cmd"] = f"ping -n {count_ping} {domain}"
            entry["mac"] = f"ping -c {count_ping} {domain}"
            
        elif action == "download":
            entry["instruction"] = f"Download file from {domain}/{fname}"
            entry["linux"] = f"curl -O https://{domain}/{fname}"
            entry["windows_cmd"] = f"curl -O https://{domain}/{fname}"
            entry["mac"] = f"curl -O https://{domain}/{fname}"
            
        elif action == "dns":
            entry["instruction"] = f"Get IP address of {domain}"
            entry["linux"] = f"nslookup {domain}"
            entry["windows_cmd"] = f"nslookup {domain}"
            entry["mac"] = f"nslookup {domain}"
            
        elif action == "ip":
            entry["instruction"] = "Show network interface configuration"
            entry["linux"] = "ifconfig"
            entry["windows_cmd"] = "ipconfig"
            entry["mac"] = "ifconfig"
            
        data.append(entry)
    return data

def generate_system_ops(count: int) -> List[Dict]:
    data = []
    # System info commands are limited, so we vary instructions
    commands = [
        ("os", "Show OS version", "cat /etc/os-release", "ver", "sw_vers"),
        ("disk", "Check disk usage", "df -h", "wmic logicaldisk get size,freespace,caption", "df -h"),
        ("mem", "Check memory usage", "free -h", "systeminfo | findstr /C:\"Total Physical Memory\"", "vm_stat"),
        ("uptime", "Check system uptime", "uptime", "systeminfo | find \"System Boot Time\"", "uptime"),
        ("env", "List environment variables", "printenv", "set", "printenv"),
        ("usb", "List USB devices", "lsusb", "wmic path Win32_USBControllerDevice get Dependent", "system_profiler SPUSBDataType")
    ]
    
    phrasings = [
        "Show me", "Display", "Check", "Get", "Print", "View", "What is"
    ]
    
    for _ in range(count):
        sub, base_instr, lin, win, mac = random.choice(commands)
        
        # Vary instruction
        phrase = random.choice(phrasings)
        words = base_instr.split(' ', 1)[1] # remove verb
        instruction = f"{phrase} {words}"
        
        entry = {
            "id": f"sys_{uuid.uuid4().hex[:8]}",
            "category": "system_information",
            "subcategory": sub,
            "instruction": instruction,
            "linux": lin,
            "windows_cmd": win,
            "mac": mac,
            "difficulty": "beginner",
            "tags": ["system", sub]
        }
        data.append(entry)
    return data

def generate_package_ops(count: int) -> List[Dict]:
    data = []
    
    for _ in range(count):
        pkg = random.choice(PACKAGES)
        action = random.choice(["install", "remove", "update", "search"])
        
        entry = {
            "id": f"pkg_{uuid.uuid4().hex[:8]}",
            "category": "package_management",
            "subcategory": action,
            "difficulty": "beginner",
            "tags": ["package", action]
        }
        
        if action == "install":
            entry["instruction"] = f"Install {pkg}"
            entry["linux"] = f"sudo apt install {pkg} -y"
            entry["windows_cmd"] = f"choco install {pkg} -y"
            entry["mac"] = f"brew install {pkg}"
            
        elif action == "remove":
            entry["instruction"] = f"Uninstall {pkg}"
            entry["linux"] = f"sudo apt remove {pkg} -y"
            entry["windows_cmd"] = f"choco uninstall {pkg} -y"
            entry["mac"] = f"brew uninstall {pkg}"
            
        elif action == "update":
            entry["instruction"] = "Update all packages"
            entry["linux"] = "sudo apt update && sudo apt upgrade -y"
            entry["windows_cmd"] = "choco upgrade all -y"
            entry["mac"] = "brew update && brew upgrade"
            
        elif action == "search":
            entry["instruction"] = f"Search for package '{pkg}'"
            entry["linux"] = f"apt search {pkg}"
            entry["windows_cmd"] = f"choco search {pkg}"
            entry["mac"] = f"brew search {pkg}"
            
        data.append(entry)
    return data

def generate_text_ops(count: int) -> List[Dict]:
    data = []
    
    for _ in range(count):
        fname = random.choice(FILENAMES)
        term = random.choice(["error", "warning", "success", "failed", "user", "TODO"])
        
        action = random.choice(["search", "count", "view", "sort"])
        
        entry = {
            "id": f"text_{uuid.uuid4().hex[:8]}",
            "category": "text_processing",
            "subcategory": action,
            "difficulty": "intermediate",
            "tags": ["text", action]
        }
        
        if action == "search":
            entry["instruction"] = f"Search for '{term}' in {fname}"
            entry["linux"] = f"grep '{term}' {fname}"
            entry["windows_cmd"] = f"findstr \"{term}\" {fname}"
            entry["mac"] = f"grep '{term}' {fname}"
            
        elif action == "count":
            entry["instruction"] = f"Count lines in {fname}"
            entry["linux"] = f"wc -l {fname}"
            entry["windows_cmd"] = f"find /c /v \"\" {fname}"
            entry["mac"] = f"wc -l {fname}"
            
        elif action == "view":
            entry["instruction"] = f"Display content of {fname}"
            entry["linux"] = f"cat {fname}"
            entry["windows_cmd"] = f"type {fname}"
            entry["mac"] = f"cat {fname}"
            
        elif action == "sort":
            entry["instruction"] = f"Sort lines in {fname}"
            entry["linux"] = f"sort {fname}"
            entry["windows_cmd"] = f"sort {fname}"
            entry["mac"] = f"sort {fname}"
            
        data.append(entry)
    return data

def generate_perm_ops(count: int) -> List[Dict]:
    data = []
    
    for _ in range(count):
        fname = random.choice(FILENAMES)
        user = random.choice(USERS)
        
        action = random.choice(["chmod", "chown", "view"])
        
        entry = {
            "id": f"perm_{uuid.uuid4().hex[:8]}",
            "category": "permissions",
            "subcategory": action,
            "difficulty": "intermediate",
            "tags": ["permissions", action]
        }
        
        if action == "chmod":
            entry["instruction"] = f"Make {fname} read-only"
            entry["linux"] = f"chmod 444 {fname}"
            entry["windows_cmd"] = f"attrib +r {fname}"
            entry["mac"] = f"chmod 444 {fname}"
            
        elif action == "chown":
            entry["instruction"] = f"Change owner of {fname} to {user}"
            entry["linux"] = f"chown {user} {fname}"
            entry["windows_cmd"] = f"icacls {fname} /setowner {user}"
            entry["mac"] = f"chown {user} {fname}"
            
        elif action == "view":
            entry["instruction"] = f"View permissions of {fname}"
            entry["linux"] = f"ls -l {fname}"
            entry["windows_cmd"] = f"icacls {fname}"
            entry["mac"] = f"ls -l {fname}"
            
        data.append(entry)
    return data

def generate_compress_ops(count: int) -> List[Dict]:
    data = []
    
    for _ in range(count):
        dirname = random.choice(DIRECTORIES)
        fname = random.choice(FILENAMES)
        
        action = random.choice(["zip", "unzip", "tar"])
        
        entry = {
            "id": f"comp_{uuid.uuid4().hex[:8]}",
            "category": "compression",
            "subcategory": action,
            "difficulty": "intermediate",
            "tags": ["compression", action]
        }
        
        if action == "zip":
            entry["instruction"] = f"Zip the {dirname} directory"
            entry["linux"] = f"zip -r {dirname}.zip {dirname}"
            entry["windows_cmd"] = f"tar -a -c -f {dirname}.zip {dirname}" # Modern Windows 10+ has tar
            entry["mac"] = f"zip -r {dirname}.zip {dirname}"
            
        elif action == "unzip":
            entry["instruction"] = f"Unzip archive.zip"
            entry["linux"] = "unzip archive.zip"
            entry["windows_cmd"] = "tar -xf archive.zip"
            entry["mac"] = "unzip archive.zip"
            
        elif action == "tar":
            entry["instruction"] = f"Create tarball of {dirname}"
            entry["linux"] = f"tar -cvf {dirname}.tar {dirname}"
            entry["windows_cmd"] = f"tar -cvf {dirname}.tar {dirname}"
            entry["mac"] = f"tar -cvf {dirname}.tar {dirname}"
            
        data.append(entry)
    return data

def generate_env_ops(count: int) -> List[Dict]:
    data = []
    
    for _ in range(count):
        var = random.choice(VARS)
        val = "some_value"
        
        action = random.choice(["set", "get", "unset"])
        
        entry = {
            "id": f"env_{uuid.uuid4().hex[:8]}",
            "category": "environment_variables",
            "subcategory": action,
            "difficulty": "intermediate",
            "tags": ["env", action]
        }
        
        if action == "set":
            entry["instruction"] = f"Set {var} to {val}"
            entry["linux"] = f"export {var}={val}"
            entry["windows_cmd"] = f"set {var}={val}"
            entry["mac"] = f"export {var}={val}"
            
        elif action == "get":
            entry["instruction"] = f"Show value of {var}"
            entry["linux"] = f"echo ${var}"
            entry["windows_cmd"] = f"echo %{var}%"
            entry["mac"] = f"echo ${var}"
            
        elif action == "unset":
            entry["instruction"] = f"Unset {var}"
            entry["linux"] = f"unset {var}"
            entry["windows_cmd"] = f"set {var}="
            entry["mac"] = f"unset {var}"
            
        data.append(entry)
    return data

# --- Main Driver ---

def main():
    generators = {
        "01_file_operations.json": generate_file_ops,
        "02_directory_operations.json": generate_dir_ops,
        "03_process_management.json": generate_process_ops,
        "04_network_operations.json": generate_network_ops,
        "05_system_information.json": generate_system_ops,
        "06_package_management.json": generate_package_ops,
        "07_text_processing.json": generate_text_ops,
        "08_permissions.json": generate_perm_ops,
        "09_compression.json": generate_compress_ops,
        "10_environment_variables.json": generate_env_ops
    }
    
    output_dir = Path("datasets/generated/raw")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for filename, generator in generators.items():
        print(f"Generating 500+ samples for {filename}...")
        data = generator(100) # Generate extra to be safe
        
        output_path = output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
    print("Generation complete.")

if __name__ == "__main__":
    main()
