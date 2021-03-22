import click
from training.services import svc_report_data as data
from training.services import svc_report_maker as report_maker
from training.services import svc_reporter as reporter

@click.group()
def cli():
    """Course report options for 40hr Moodle Courses"""
    pass

@cli.command()
def grade_courses():
    """Open all courses listed in course_id.csv to course report page at dstrainings for grading.
    Must be logged in prior."""
    data.grade_courses()


@cli.command()
def get_files():
    """Gets all course completion reports from dstrainings.com as csv.
    Must be logged in prior."""
    data.get_csv()


@cli.command()
@click.option("-c", "--get_csv", is_flag=True, help="Flag that, when enabled, downloads course completion csv files.")
@click.option("-e", "--export_combined", is_flag=True, help="Flag that, when enabled, exports a combined csv for each month. Can be used for email status updates.")
def full_run(get_csv, export_combined):
    """Takes all completion reports from Downloads file, combines as needed and
    moves to archive (Data{Date})"""
    reporter.main_program(get_csv, export_combined)


@cli.command()
@click.option("-e", "--export_combined", is_flag=True, help="Flag that, when enabled, exports a combined csv for each month. Can be used for email status updates.")
def single_course(get_csv, export_combined):
    """Run a single report, assuming one month of files is in either downloads or data directories. Often for troubleshooting or rechecking."""
    reporter.run_single_report()
