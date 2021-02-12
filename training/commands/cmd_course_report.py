import click


class Context:
    def __init__(self, month):
        self.month = month

@click.group()
@click.option("-m","--month", type=str, help="Month of course you want reported.")
@click.pass_context
def cli(ctx):
    """Run course reports for Moodle Completion csv's"""
    ctx.obj = Context(month)
    pass

@click.command()
@click.pass_context
def run_full_report(ctx):
    """Run course reports for all months."""
    pass

@click.command()
@click.pass_context
def run_single_month(ctx):
    """Run a course report for a given month"""
    month = ctx.obj.month
    pass

@click.command()
@click.pass_context
def run_report_remind(ctx):
    """Run the all months and prepare reminder emails for staff not finished."""
    pass
