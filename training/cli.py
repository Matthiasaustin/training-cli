import os
import logging
import click
import config

main_dir = config.main_path()

logger = logging.getLogger(__name__)
formatter = logging.Formatter("%(asctime)s:%(name)s:%(message)s")

file_handler = logging.FileHandler(main_dir / "training_cli.log")
stream_handler = logging.StreamHandler()

file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


class ComplexCLI(click.MultiCommand):
    def list_commands(self, ctx):
        commands = []
        commands_folder = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "commands")
        )
        for filename in os.listdir(commands_folder):
            if filename.endswith(".py") and filename.startswith("cmd_"):
                commands.append(filename.replace("cmd_", "").replace(".py", ""))

        commands.sort()
        return commands

    def get_command(self, ctx, name):
        try:
            mod = __import__(f"training.commands.cmd_{name}", None, None, ["cli"])
        except ImportError:
            logger.exception("Import Error has occurred.")
            return
        return mod.cli


@click.command(cls=ComplexCLI)
def cli():
    """Welcome to Training Helper! An all-in-one cli task assistant!"""
    pass
