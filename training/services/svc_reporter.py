"""
Main program of the training reporter suite. The program onces complete will serve as the hub and "ui" through cli for various programs/modules for compiling reports and emailing staff/students
"""
import pandas as pd
import glob
import shutil
from pathlib import Path
from datetime import datetime
import training.services.svc_report_data as data
import training.services.svc_report_maker as report_maker
import training.services.svc_completion as completion
import config


main_dir = config.main_path()


def main_program(get_csv=None, export_combined=None):
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #
    # Need to add relative paths to data, export and downloads here to there
    # aren't conflicts on local program runs. Add arguments for any function
    # that locates files and add to local/global run times.
    #
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    if get_csv is not None:
        get_csv = input("get new csv? y/n \n")
        if get_csv.lower() == "y":
            data.get_csv()
            input("press any key when finished downloading.")
    elif get_csv == "y":
        data.get_csv()
        input("press any key when finished downloading.")
    elif get_csv != "y" and get_csv is not None:
        raise Exception("Unknown Input for get_csv.")
    else:
        print("Not getting csv files.")
        pass

    data_dir = main_dir / "data"
    download_dir = Path.home() / "Downloads"
    date = datetime.now().strftime("%Y%m%d")
    current_month = datetime.now().date().strftime("%B").lower()

    last_checked = data.log_check().strftime("%Y-%m-%d %H:%M")
    # make a directory for the data from today
    archive_dir = data_dir / f"Data{date}"
    try:
        Path(archive_dir).mkdir(exist_ok=True)
        print("Folder Made")
    except FileExistsError:
        print("Folder Already Made")
        pass
    else:
        print("Folder Made, Ready.")
    rerun = True
    records = []
    while rerun:
        # assign archive folder
        archive = data_dir / f"Data{date}"
        download_dir = Path.home() / "Downloads"

        download_files = download_dir.glob("completion-*")
        months = []
        master = pd.DataFrame()
        for f in download_files:
            f = str(f)
            months.append(data.get_month(f))
            months = list(set(months))
        for month in months:
            csv = data.import_data(month, data_dir, download_dir)
            record = report_maker.parse_data(csv, export_combined=None)
            master.append(record)
            print(record[0])
            print(record[1])
            record[0],record[1] = completion.check_completion(record[0],last_checked), completion.check_completion(record[1],last_checked)
            data.export_to_excel(record)
            sola, voa, combined_report = record
            records.append(combined_report)
            for f in data_dir.glob("*.csv"):
                f.rename(archive / f.name)
        rerun = input("Rerun? yes or no\n").lower()
        if rerun.lower() == "yes" or rerun.lower() == "y":
            rerun = True
            for f in archive.glob("*.csv"):
                f.rename(download_dir / f.name)
        else:
            rerun = False

        #added to reset csv data files during testing.
        # for f in archive.glob("*.csv"):
        #     f.rename(download_dir / f.name)
        # Combine and format the collected VOA records in one df
        c_rec = pd.concat(records)
        export_dir = main_dir / "export"
        # c_rec = data.prep_df(c_rec)
        c_rec = c_rec.reset_index()
        c_rec = c_rec.reindex(
            columns=[
                "Department",
                "Name",
                "Email address",
                "Institution",
                "ID number",
                "Month",
                "Chapter 1",
                "Chapter 2",
                "Chapter 3",
                "Due Date #1",
                "Chapter 4",
                "Chapter 13",
                "Chapter 14",
                "Due Date #2",
                "Chapter 5",
                "Chapter 6",
                "Chapter 7",
                "Due Date #3",
                "Chapter 8",
                "Chapter 11",
                "Due Date #4",
                "Chapter 9",
                "Chapter 10",
                "Chapter 12",
                "Due Date #5",
                # "Chapter 12 Skills Lab",
                "Total Hours Completed",
                "Hours Completed Since Last Check",
                "Total Hours Outstanding",
            ]
        )

        c_rec = completion.check_completion(c_rec,last_checked)
        c_rec.to_csv(export_dir / "master.csv")
        # print(c_rec)
        # # print(records[0])
        # # print("\n*** Records List Start ***\n",records,"\n*** Records End ***\n")
        # for i in records[1:-1]:
        #     # print(i,"#########\n")
        #     c_rec.append(i)
        print(c_rec)

    #added to reset csv data files during testing.
    # for f in archive.glob("*.csv"):
    #     f.rename(download_dir / f.name)


def run_single_report(export_combined=None):
    data_dir = main_dir / "data"
    date = datetime.now().strftime("%Y%m%d")
    download_dir = Path.home() / "Downloads"
    # downloads = download_dir.glob("completion-*")
    month = input("Month?\n").lower()
    csv = data.import_data(month, data_dir, download_dir)
    records = report_maker.parse_data(csv, export_combined)
    data.export_to_excel(records)
    files = data_dir.glob("*.csv")
    move = input("Move to archive? y/n\n")
    archive = data_dir / f"Data{date}"
    if move.lower() == "y":
        for f in files:
            shutil.move(f, archive)
    # email.import_info("mar_new_user_import.csv","freminder")


if __name__ == "__main__":

    print("Welcome to Trainer Hub['working title']")
    main_program()
    # run_single_report()
