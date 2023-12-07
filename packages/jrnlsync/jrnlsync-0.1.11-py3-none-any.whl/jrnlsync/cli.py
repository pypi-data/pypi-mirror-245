import click
import subprocess
from .config import read_config, read_jrnl_config, create_default_config


@click.group(invoke_without_command=True)
@click.pass_context
@click.option("-m", "--message", default="jrnlsync auto commit", type=str)
@click.argument('args', nargs=-1, type=str)
def cli(ctx, message, args):

    config = read_config()
    jrnl_folder = config.get("jrnl_folder")
    
    if ctx.invoked_subcommand is None:
        click.echo('I was invoked without subcommand')
        # TODO: continue with git logic:
        if not args:
            click.echo("no args")
            # \-> no commands: sync using git
            p = subprocess.run(["git", "pull"], cwd=jrnl_folder)
            p = subprocess.run(["git", "commit", "-am", message], cwd=jrnl_folder)
            p = subprocess.run(["git", "push"], cwd=jrnl_folder)

        elif args:
            # \-> with commands: assume git command
            click.echo(f"with args {args}")
            p = subprocess.run(["git"] + list(args), cwd=jrnl_folder)
            return p
        else:
            # This should not happen
            raise Exception("Something strange is happening")
        
    else:
        click.echo(f"I am about to invoke {ctx.invoked_subcommand}")
        # TODO: create subcommand logic
    return

@cli.command()
@click.argument('args', nargs=-1, type=str)
def git(args):
    config = read_config()
    jrnl_folder = config.get("jrnl_folder")

    p = subprocess.run(["git"] + list(args), cwd=jrnl_folder)
    return

@cli.command()
@click.argument("journal", default="default", type=str)
def open(journal):
    # TODO: continue with open command
    jrnl_config = read_jrnl_config()
    click.echo(f"Open jrnl file for {journal}")
    journals = jrnl_config.get("journals")
    journal_path = journals.get(journal)
    click.echo(f"journal path: {journal_path}")
    editor_path = jrnl_config.get("editor")
    click.echo(f"using editor: {editor_path}")
    p = subprocess.run([editor_path, journal_path])
    return

@cli.command()
@click.pass_context
def merge(ctx):
    click.echo("This function is currently not implemented")
    # TODO: create function that resolves merge conflicts