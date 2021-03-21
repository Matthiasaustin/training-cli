import click
from training.services import svc_email as email
from pathlib import Path

# class Context:
#     def __init__():
#         self.message = svc_email.Message()


# @click.group()
# def cli():
#     pass


@click.command()
@click.option("-f", "--file_name", type=str, help="The file to be used for staff name and emails.")
@click.option("-m", "--message_type", type=str, help="Type of message to be sent (i.e. CPR Start off email, Forty Hour reminder email, etc.)")
def cli(file_name, message_type):
    """Send an email based on a csv info file and html template."""
    email.start(csv_name=file_name, message_type=message_type)

    pass
