import os
import json

FILE_SYSTEM = {
    '/': {}  
}


CWD = '/'

def mkdir(dir_path):
    paths = dir_path.split('/')
    curr_dir = FILE_SYSTEM
    for p in paths:
        if p not in curr_dir:
            curr_dir[p] = {}
        curr_dir = curr_dir[p]

def ls(dir_path=None):
    """List contents of directory"""
    global CWD
    if dir_path is None:
        dir_path = CWD  
    node = get_dir(dir_path)
    if node:
        print(*list(node.keys()), sep="\n") 

def get_dir(dir_path):
    paths = dir_path.replace('/', ' ').strip().split(' ')
    node = FILE_SYSTEM
    for p in paths:
        if p == '..':
            node = FILE_SYSTEM if node is FILE_SYSTEM else node = list(FILE_SYSTEM.keys())[list(FILE_SYSTEM.values()).index(node)]
        elif p in node:
            node = node[p]
        else:
            print(f"cd: no such file or directory: {p}")
            return None
    return node

def cd(dir_path): 
    global CWD 
    node = get_dir(dir_path)
    if node:
        CWD = dir_path

def touch(filename):
    global CWD  
    if filename not in FILE_SYSTEM[CWD]:
        FILE_SYSTEM[CWD][filename] = '' 

def echo(text, filename):
    global CWD
    if filename not in FILE_SYSTEM[CWD]:
        print(f"{filename}: No such file")
    else:
        FILE_SYSTEM[CWD][filename] = text

def cp(src, dest):
    if not os.path.exists(src):
        print(f"cp: '{src}' does not exist")
        return

    if os.path.isdir(src):
        print("cp: recursive copy not supported yet")
        return

    if not os.path.exists(os.path.dirname(dest)): 
        print(f"cp: '{os.path.dirname(dest)}' does not exist")
        return

    FILE_SYSTEM[os.path.dirname(dest)][os.path.basename(dest)] = FILE_SYSTEM[os.path.dirname(src)][os.path.basename(src)]

def mv(src, dest):
    if not os.path.exists(src):
        print(f"mv: '{src}' does not exist")
        return

    if os.path.isdir(src):
        print("mv: moving directories not supported yet")
        return

    if not os.path.exists(os.path.dirname(dest)):
        print(f"mv: '{os.path.dirname(dest)}' does not exist") 
        return

    FILE_SYSTEM[os.path.dirname(dest)][os.path.basename(dest)] = FILE_SYSTEM[os.path.dirname(src)].pop(os.path.basename(src))

def rm(path):
    if not os.path.exists(path):
        print(f"rm: '{path}' does not exist")
        return

    if os.path.isdir(path):
        print("rm: recursive removal not supported yet") 
        return
    
    del FILE_SYSTEM[os.path.dirname(path)][os.path.basename(path)]
    
def save_state(path):
    with open(path, 'w') as f:
        json.dump(FILE_SYSTEM, f)

def load_state(path):
    global FILE_SYSTEM
    with open(path) as f:
        FILE_SYSTEM = json.load(f)

if __name__ == "__main__":

    running = True
    
    print("Welcome to in-memory file system!")
    print("Type 'help' for list of supported commands\n")
    
    while running:
        
        inp = input(f"{CWD} $ ").strip()
        
        if inp == "exit":
            running = False
            
        elif inp.startswith("mkdir"):
            mkdir(inp[6:].strip())
            
        elif inp.startswith("ls"):
            ls(inp[3:].strip())
            
        
        elif inp == "help":
            print("Supported commands:")
            print("mkdir <dir> - Make directory")
            print("ls <dir> - List directory content")
            print("cd <dir> - Change directory")
            print("grep <dir> - Search for a specified pattern in a file")
            print("cat <dir> - Display the contents of a file")
            print("touch <dir> - Create a new empty file")
            print("echo <dir> - write text to a file")
            print("mv <dir> - copy a file or directory to another location")
            print("rm <dir> - Remove a file or directory")