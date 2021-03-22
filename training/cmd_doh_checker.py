import click
from training.services import svc_checker

# class Context:
#     def __init__(self):
#         self.program_name = "Credential Finder"

# @click.pass_context()
@click.group()
def cli():
    pass


@cli.command()
@click.option("-f", "--first_name", type=str, help="First Name")
@click.option("-l", "--last_name", type=str, help="Last Name")
@click.option("-b", "--birthday", type=str, help="Birthday")
@click.option("-c", "--credential_number", type=str, help="Credential Number")
# @click.pass_context()
def check_one():
    """Check a single record"""
    results = svc_checker.Check().check_single_record(
        first_name="Eric Joseph", last_name="Tagle", birthday="11/20/1986"
    )
    for result in results:
        click.echo(result)

    results = svc_checker.Check().check_single_record(
        first_name="Ebrima", last_name="Ceesay", birthday="3/3/1982"
    )
    for result in results:
        click.echo(result)
        # click.echo(r,v)
    # click.echo("Results")


@cli.command()
def check_all():
    click.echo("Check all starting")


if __name__ == "__main__":
    cli()
