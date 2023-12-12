import click
from pathlib import Path
import tomllib
import os
import time
import re
import numpy as np
from glob import glob
import subprocess
from datetime import datetime
import importlib.metadata

#  ──────────────────────────────────────────────────────────────────────────
# global variables

douglog_version = importlib.metadata.version('douglog')
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.command(context_settings=CONTEXT_SETTINGS)

#  ──────────────────────────────────────────────────────────────────────────
# global functions

def logbook_not_found(logbook):
    click.echo(logbook + ' logbook not found in config.')
    exit()

#  ──────────────────────────────────────────────────────────────────────────
# base command

# done for the config
@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.version_option(douglog_version)
@click.option('-c', '--config', default='~/.config/dlog.toml', type=str, help="Config file path", show_default=True)
@click.pass_context
def dlog(ctx, config):
    """Simple and quick logging program."""

    ctx.ensure_object(dict)

    config = Path(config).expanduser()
    if config.exists():

        with open(config, 'rb') as file:
            toml = tomllib.load(file)

        # required config options
        required = ['logbooks']
        for option in required:
            if option not in toml:
                click.echo('Config requires "' + key + '" to be set.')
                exit()

        # home log directory
        if 'home' in toml:
            ctx.obj['home'] = Path(toml['home']).expanduser()
        else:
            ctx.obj['home'] = Path('~/dlogs').expanduser()

        # individual logs
        ctx.obj['logbooks'] = []
        for logbook in toml['logbooks']:
            ctx.obj['logbooks'].append(logbook)

            logbook_path = ctx.obj['home'] / Path(logbook)

            if not logbook_path.exists():
                os.mkdir(logbook_path)

        # editor
        if 'editor' in toml:
            ctx.obj['editor'] = toml['editor']
        else:
            ctx.obj['editor'] = 'vim'

    else:
        click.echo('No config file, exiting.')
        exit()

#  ──────────────────────────────────────────────────────────────────────────
# log command to generate single logs

@dlog.command('log', short_help='Open a new log in your editor.',context_settings=CONTEXT_SETTINGS)
@click.argument('logbook', type=str)
@click.pass_context
def log(ctx, logbook):
    """Open a new log in LOGBOOK in your editor."""

    if logbook in ctx.obj['logbooks']:
        logbook_path = ctx.obj['home'] / Path(logbook)

        epoch = str(np.floor(time.time()).astype(np.int64))
        date = time.strftime("%a, %d %b %Y %H:%M:%S UTC", time.gmtime())

        file_path = logbook_path / Path(epoch + '.md')
        with open(file_path, 'a') as file:
            file.write('# ' + date + '\n')

        # editting 
        click.edit(filename=file_path, editor=ctx.obj['editor'])

        # committing 
        git_path = logbook + '/' + file_path.name
        ctx.invoke(git, git_commands=['add', git_path])
        ctx.invoke(git, git_commands=['commit', '-m', '"Added ' + git_path + '"'])

    else:
        logbook_not_found(logbook)

#  ──────────────────────────────────────────────────────────────────────────
# list command to list logs

@dlog.command(context_settings=CONTEXT_SETTINGS)
@click.option('-l', '--logs', default=False, help='List logs as well.', is_flag=True)
@click.pass_context
def list(ctx, logs):
    """Lists all logbooks."""

    for logbook in ctx.obj['logbooks']:
        click.echo(logbook)
        
        if logs:
            logbook_path = ctx.obj['home'] / Path(logbook)
            file_paths = sorted(logbook_path.glob('*.md'))

            for file_path in file_paths:

                date = datetime.utcfromtimestamp(int(file_path.stem)).isoformat()
                click.echo(file_path.name + ' : ' + date)

            click.echo()

    exit()

#  ──────────────────────────────────────────────────────────────────────────
# search command

@dlog.command('search', short_help='Searches through your logs.', context_settings=CONTEXT_SETTINGS)
@click.option('-l', '--logbook', type=str, help="Specified logbook to search.", default=None)
@click.argument('regex', type=str)
@click.pass_context
def search(ctx, regex, logbook):
    """
    Searches through your logs for the given REGEX. Searches through all logs unless one is specified. Results are printed as:

    logbook: filename: date: line number: line
    """

    def inbook(ctx, logbook, regex):

        logbook_path = ctx.obj['home'] / Path(logbook)
        file_paths = sorted(logbook_path.glob('*.md'))

        for file_path in file_paths:

            date = datetime.utcfromtimestamp(int(file_path.stem)).isoformat()

            with open(file_path, 'r') as file:

                for i, line in enumerate(file):

                    if re.search(regex, line):
                        found_line = logbook + ': ' + file_path.stem + ': ' + date + ': ' + str(i + 1) + ': ' + line.strip('\n')
                        click.echo(found_line)


    if logbook:
        if logbook in ctx.obj['logbooks']:
            inbook(ctx, logbook, regex)
        else:
            logbook_not_found(logbook)

    else:
        for logbook in ctx.obj['logbooks']:
            inbook(ctx, logbook, regex)

#  ──────────────────────────────────────────────────────────────────────────
# git command

CONTEXT_SETTINGS_git = CONTEXT_SETTINGS.copy()
CONTEXT_SETTINGS_git['ignore_unknown_options'] = True

@dlog.command('git', short_help='Git manage the logbooks.', context_settings=CONTEXT_SETTINGS_git)
@click.argument('git_commands', type=click.UNPROCESSED, nargs=-1)
@click.pass_context
def git(ctx, git_commands):
    """Git command to manage the douglog git repository."""

    command = ['git', '-C', ctx.obj['home']]

    for arg in git_commands:
        command.append(arg)

    subprocess.run(command)

#  ──────────────────────────────────────────────────────────────────────────
# delete command

@dlog.command('delete', short_help='Delete a log.', context_settings=CONTEXT_SETTINGS)
@click.argument('logbook', type=str)
@click.option('-l', '--log', type=str, default=None, help='Delete specified log.')
@click.pass_context
def delete(ctx, logbook, log):
    """Delete a log from the LOGBOOK. Deletes the most recent log if none is specified."""

    if logbook in ctx.obj['logbooks']:
        logbook_path = ctx.obj['home'] / Path(logbook)
        file_paths = sorted(logbook_path.glob('*.md'))

        if log:
            log_path = logbook_path / Path(log)
            if log_path in file_paths:
                delete_log = log_path
            else:
                click.echo('Log specified but not found.')
                exit()
        else:
            delete_log = file_paths[-1]

        if click.confirm('Do you want to delete: ' + logbook + '/' + delete_log.name + '?'):
            click.echo('Deleting ' + delete_log.name + ' in ' + logbook)
            subprocess.run(['rm', delete_log])

            # committing 
            git_path = logbook + '/' + delete_log.name
            ctx.invoke(git, git_commands=['add', git_path])
            ctx.invoke(git, git_commands=['commit', '-m', '"Deleted ' + git_path + '"'])

    else:
        logbook_not_found(logbook)
