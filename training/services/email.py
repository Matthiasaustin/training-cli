# import win32com.client as win32
import pandas as pd
import jinja2
import os
import glob
from datetime import datetime

class Message():
    def __init__(self, df_row):
        recipient = df_row[0]
        self.name = ""
        self.message_type = ""
        self.template = ""
        self.outputText = "None has been specified. Please run a constructor"

        templateLoader = jinja2.FileSystemLoader(searchpath="../email_data/templates")
        templateEnv = jinja2.Environment(loader=templateLoader)

    def cpr_start_email():
        self.email = str(recipient['personal_email'])
        self.supervisor_email = str(recipient['sup_email'])
        self.attachement = None
        self.name = str(recipient['first_name'])
        self.link = str(recipient['registration_link'])
        self.close_date = str(recipient['closing_date'])
        self.template_file = 'cpr_email.html'
        date = datetime.now()
        date = date.strftime("%m/%d/%Y")
        self.subject = f"CPR/First Aid Required - {date}"
        template = templateEnv.get_template(template_file)
        name = self.name
        link = self.link
        close_date = self.close_date
        outputText = template.render(name=name,  # Include args for render
                                     link=link,
                                     close_date=close_date)

    def fhr_start_email():
        self.email = str(recipient['email'])
        self.supervisor_email = str(recipient['profile_field_supervisor_email'])
        self.attachment = PATH = os.path.abspath("../email_data/attachments/feb_2021_syllabus.pdf")
        self.template_file = 'welcome_40hr.html'
        self.name = str(recipient['firstname'])
        self.month = "February"
        self.subject = f"Welcome to the {month} 40hr Core"
        self.username = str(recipient['username'])
        self.password = str(recipient['password'])
        self.template = templateEnv.get_template(template_file)
        name = self.name
        month = self.month
        username = self.username
        password = self.password
        self.outputText = template.render(name=name,  # Include args for render
                                          month=month,
                                          username=username,
                                          password=password)

    def fhr_reminder_email():
        fhr_start_email()
        date = datetime.now()
        date = date.strftime("%m/%d/%Y")
        self.subject = f"Training Reminder/Update - {date}"
        self.template_file = 'reminder_40hr.html'
        self.template = templateEnv.get_template(template_file)
        self.outputText = template.render(name=name,  # Include args for render
                                          month=month)
    def get_body():
        return self.outputText


def get_message(recipient, message_type):
    message_type = message_type
    templateLoader = jinja2.FileSystemLoader(searchpath="../email_data/templates")
    templateEnv = jinja2.Environment(loader=templateLoader)


# Currently windows only, may try to make system agnostic at somepoint
def make_email(recipient, subject, message_type):
    subject = subject
    message_type = message_type
    message = Message(recipient[1])
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)

    if message_type == 'cpr':
        message.cpr_start_email()
    elif message_type == 'fstart':
        message.fhr_start_email()
    elif message_type == 'freminder':
        message.fhr_reminder_email()

    mail.To = message.email
    mail.CC = message.supervisor_email
    text = message.get_body()
    subject = str(subject)

    mail.Subject = subject
    if message.attachment != None:
        mail.Attachments.Add(Source=message.attachment)
    mail.HtmlBody = text

    mail.Save()

def list_send_info():
    rv = []
    for filename in os.listdir(os.path.abspath('../email_data/send_info/')):
        if filename.endswith(".csv"):
            rv.append(filename[0:-4])
    rv.sort()
    return rv

# import_address
def import_info():

    default_send_info = 'feb_new_user_import.csv'
    PATH = os.path.abspath('../email_data/send_info/')

    filename = input("Which of the above would you like to use?")
    joined = os.path.join(PATH,f"*{filename}.csv")
    files = glob.glob(joined)
    while len(files) > 1:
        for file in files:
            print(os.path.basename(file))
        print("There is more than one file. Please select one:")
        input("Which one?")
        joined = os.path.join(PATH,f"*{filename}.csv")
        files = glob.glob(joined)

    print(PATH)
    default_input_message = """
    Which would message?
    cpr
    fwelcome (40hr Welcome message)
    freminder (40hr Reminder message)
    """

    message_type = input(default_input_message)
    recipients = pd.read_csv(PATH)
    subject = input("What is the message subject?\n")
    for row in recipients.iterrows():
        make_email(row, subject, message_type)


if __name__ == "__main__":
    print(list_send_info())
    PATH = os.path.abspath('../email_data/send_info/')
    filename = input("Which of the above would you like to use?")
    joined = os.path.join(PATH,f"*{filename}.csv")
    files = glob.glob(joined)
    if len(files) > 1:
        for file in files:
            print(os.path.basename(file))
        print("There is more than one file. Please select one:")
        input("Which one?")
        joined = os.path.join(PATH,f"*{filename}.csv")
        files = glob.glob(joined)
