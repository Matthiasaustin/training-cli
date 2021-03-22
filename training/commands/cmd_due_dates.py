import click
from training.services import svc_due_date_checker as due_date

@click.group()
def cli():
    pass



@cli.command()
def cpr():
    """Put together a due date list for staff CPR"""
    due_date.get_due_date_list(report_type="CPR")


@cli.command()
def bbp():
    due_date.get_due_date_list(report_type="BBP")


@cli.command()
def mandated():
    due_date.get_due_date_list(report_type="Mandated")


@cli.command()
def continuing_education():
    due_date.get_ce()
