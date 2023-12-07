from .config import read_config, create_default_config, read_jrnl_config

import sys
import subprocess


def git(commands, cwd=None):
    config = read_config()
    jrnl_folder = cwd or config.get("jrnl_folder")
    return subprocess.run(["git"] + commands, cwd=jrnl_folder)


def sync_journals(commit_message="jnrlsync automated commit"):
    git(["pull"])
    git(["commit", "-am", commit_message])
    git(["push"])
    return


def main():
    args = sys.argv[1:]
    
    if not args:
        sync_journals()

    elif args:

        if args[0] == "--start":
            create_default_config()
            return

        if args[0] == "git":
            args.pop(0)
            p = git(args)
            return p
        
        if args[0] in ("-m", "--message"):
            try:
                commit_message = args[1]
            except IndexError:
                commit_message = input("Please specify commit message: ")
            sync_journals(commit_message=commit_message)
            return
        
        if args[0] == "open":
            try:
                jrnl = args[1]
            except IndexError:
                jrnl = 'default'
            jrnl_config = read_jrnl_config()
            print(f"Open jrnl file for {jrnl}")
            journals = jrnl_config.get("journals")
            journal_path = journals.get(jrnl)
            editor = jrnl_config.get("editor")
            p = subprocess.run([editor, journal_path])
            return p 
        
        else:
            p = git(args)
            return p
        return
