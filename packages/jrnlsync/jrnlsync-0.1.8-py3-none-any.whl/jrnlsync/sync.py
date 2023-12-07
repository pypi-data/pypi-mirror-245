from .config import read_config, create_default_config, read_jrnl_config

import sys
import subprocess

def main():
    config = read_config()
    jrnl_folder = config.get("jrnl_folder")

    commit_message = "jnrlsync automated commit"  # Can be overridden by -m flag

    args = sys.argv[1:]
    print(args)  # breakpoint()
    if args:
        if args[0] == "--start":
            create_default_config()
            return

        if args[0] == "git":
            args.pop(0)
            p = subprocess.run(["git"] + args, cwd=jrnl_folder)

        if args[0] == "-m":
            try:
                commit_message = args[1]
            except IndexError:
                commit_message = input("Please specify commit message: ")
            
        if args[0] == "open":
            try:
                jrnl = args[1]
            except IndexError:
                jrnl = 'default'

            jrnl_config = read_jrnl_config()
            print(f"Open jrnl file for {jrnl}")
            journals = jrnl_config.get("journals")
            journal_path = journals.get(jrnl)
            p = subprocess.run([jrnl_config.get("editor"), journal_path])
            return

        p = subprocess.run(["jrnl"] + args, cwd=jrnl_folder)
   
    print("attempting default sync")
    p = subprocess.run(["git", "pull"], cwd=jrnl_folder)
    p = subprocess.run(["git", "commit", "-am", commit_message], cwd=jrnl_folder)
    p = subprocess.run(["git", "push"], cwd=jrnl_folder)
    return
    
    
    return 

