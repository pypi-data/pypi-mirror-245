"""Mara command line interface"""

import logging
import sys

import click

log = logging.getLogger(__name__)

RED = '\033[31m'
RESET = '\033[0m'


@click.group(help="""
The Mara ELT Framework is a Python framework to build data pipelines.

Contributed functionality (ETL runners, downloader,...) are available as subcommands.""")
@click.option('--debug', default=False, is_flag=True, help="Show debug output")
@click.option('--log-stderr', default=False, is_flag=True, help="Send log output to stderr")
def cli(debug: bool, log_stderr: bool):
    # --debug is consumed by the setup_commandline_commands but it's here to let it show up in help
    # and not cause parse errors
    pass


def setup_commandline_commands():
    """Needs to be run before click itself is run so the config which contributes click commands is available"""
    commandline_debug = '--debug' in sys.argv
    # makefiles expect all log in stdout. Send to stderr only if asked to
    log_stream = sys.stderr if '--log-stderr' in sys.argv else sys.stdout
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s, %(name)s: %(message)s',
                        datefmt='%Y-%m-%dT%H:%M:%S',
                        stream=log_stream)

    if commandline_debug:
        logging.root.setLevel(logging.DEBUG)
        log.debug("Enabled debug output via commandline")

    if sys.version_info < (3, 10):
        from importlib_metadata import entry_points
    else:
        from importlib.metadata import entry_points

    discovered_plugins = entry_points(group='mara.commands')
    for entry_point in discovered_plugins:
        command = entry_point.load()
        command.name = entry_point.name
        if not isinstance(command, click.Command):
            log.warn(f"Entry point '{entry_point}' is ignored because it does not return a click command.")
        else:
            cli.add_command(command)

    if not cli.commands:
        # Could not find any command in the installed modules
        print(RED + "No mara package is installed which provide commands" + RESET, file=sys.stderr)
        print("""
Please install the packages you want to use, e.g. by calling
              
    pip install mara-pipelines
""", file=sys.stderr)
        sys.exit(1)


def main():
    """'mara' console_scripts entry point"""
    setup_commandline_commands()
    args = sys.argv[1:]
    cli.main(args=args, prog_name='mara')


if __name__ == '__main__':
    main()
