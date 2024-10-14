import webbrowser
import customtkinter
from calendar_exporter import export_calendar
from scraper import request_calendar, clean_received_sessions
from utils import *
from datetime import datetime
from typing import Tuple
from tkcalendar import Calendar 

URL_CAMPUS_GLOBAL = "https://secretariavirtual.upf.edu/"
URL_IMPORT_CALENDAR = "https://calendar.google.com/calendar/r/settings/export"


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

current_frame = 0

def launch_campus_global():
    webbrowser.open(URL_CAMPUS_GLOBAL, new=2)  # 2 requires new tab


def launch_google_calendar():
    webbrowser.open(URL_IMPORT_CALENDAR, new=2)  # 2 requires new tab


def guide_user_start() -> Tuple[str, datetime, datetime, str, bool]:
    print("steps")
    print_progress_bar(0, 7)

    print("log in to Campus Global")
    input("press enter to continue and launch Campus Global...")
    launch_campus_global()
    print_progress_bar(1, 7)

    input("enter 'Els meus horaris'")
    print_progress_bar(2, 7)

    input("click 'Veure Calendari'")
    print_progress_bar(3, 7)

    print("right click, inspect (using Chrome), Application, Cookies, copy JSESSIONID")
    jsessionid = input("JSESSIONID: ")
    print_progress_bar(4, 7)

    print("customise parameters")
    first_date = ask_date("first date to import")
    last_date = ask_date("last date to import:", greater_than=int(first_date.timestamp()))
    print_progress_bar(5, 7)

    print("select directory")
    saving_path = ask_path() + "\\calendar_export"
    print_progress_bar(6, 7)

    print("additional options")
    separate = ask_yes_no("export subjects in separate files? ")
    print_progress_bar(7, 7)

    return jsessionid, first_date, last_date, saving_path, separate


def process(jsessionid: str, first_date: datetime, last_date: datetime, saving_path: str, separate: bool) -> bool:
    print_progress_bar(0, 3)

    print("posting ajax request...")
    data = request_calendar(jsessionid, str(int(first_date.timestamp())), str(int(last_date.timestamp())))
    print("...ajax request finished")
    print_progress_bar(1, 3)

    print("cleaning received info...")
    clean_received_sessions(data)
    print("...cleaning finished")
    print_progress_bar(2, 3)

    print("exporting Google Calendar file...")
    status = export_calendar(data, saving_path, separate)
    print("...exported")
    print_progress_bar(3, 3)

    return status

def process_gui(jsessionid: str, first_date: datetime, last_date: datetime, saving_path: str, separate: bool, frame, deleteframe) -> bool:
    for delete in deleteframe:
        delete.pack_forget()
    
    frame.pack(expand=True)

    steps = customtkinter.CTkLabel(master=frame, text="Posting AJAX Request...", font=("Calibri", 24))
    steps.pack(pady=12, padx=10)
    data = request_calendar(jsessionid, str(int(first_date.timestamp())), str(int(last_date.timestamp())))
    if (data == None):
        stepf = customtkinter.CTkLabel(master=frame, text="Request failed!", font=("Calibri", 24))
        stepf.pack(pady=12, padx=10)
        stepf = customtkinter.CTkLabel(master=frame, text="Check your internet connection, or if you properly copied your JSESSIONID", font=("Calibri", 16))
        stepf.pack(pady=0, padx=10)
        return
    print_progress_bar(1, 3)

    steps.configure(text="Cleaning recieved info...")
    clean_received_sessions(data)
    print("...cleaning finished")
    print_progress_bar(2, 3)

    steps.configure(text="Exporting Google Calendar file...")
    status = export_calendar(data, saving_path, separate)
    print_progress_bar(3, 3)

    steps.pack_forget()
    step4 = customtkinter.CTkLabel(master=frame, text="Task finished!", font=("Calibri", 40))
    step4.pack(pady=12, padx=10)
    border_color = "#FFCC70"
    border_width = 2
    button_google_calendar = customtkinter.CTkButton(master = frame, text = "Open Google Calendar", font=("Calibri", 24), width=250, height=50, 
                                             border_color = border_color, border_width=border_width, fg_color="transparent",
                                             command=launch_google_calendar)
    button_google_calendar.pack(pady=20, padx=10)

    return status


def guide_user_end() -> None:
    print("you can now import the file to Google Calendar")
    print("additional info:")
    print("https://support.google.com/calendar/answer/37118?co=GENIE.Platform%3DDesktop&hl=en")
    print("suggestion: create a new calendar and import it there, so that you can batch-delete/color change")
    input("press enter to import into Google Calendar manually")
    launch_google_calendar()


def show_troubleshooting_steps() -> None:
    print("- verify that you have followed the steps correctly in general")
    print("- verify that you have not added any space when entering the JSESSIONID")
    print("- verify that you have clicked 'Veure calendari' before copying the JSESSIONID and trying to request the "
          "calendar")


def login(content):
    print(content)

def next_frame(frames, b_next, b_prev):
    b_prev.grid(row=0,column=0, padx=10)
    global current_frame
    if (current_frame + 1 != len(frames)):
        frames[current_frame].pack_forget()
        current_frame += 1
        frames[current_frame].pack(expand=True)
        if (current_frame +1 == len(frames)):
            b_next.grid_forget()
    print(current_frame)

def prev_frame(frames, b_next, b_prev):
    b_next.grid(row=0,column=1, padx=10)
    global current_frame
    if (current_frame - 1 != -1):
        frames[current_frame].pack_forget()
        current_frame -= 1
        frames[current_frame].pack(expand=True) 
        if (current_frame - 1 == -1):
            b_prev.grid_forget()
    print(current_frame)


def frame_start(welcome, frame, bottom_frame):
    welcome.pack_forget()
    frame.pack(expand=True)
    bottom_frame.pack(side="bottom", pady=10)

    

def frame_config(root, app):
    border_color = "#FFCC70"
    border_width = 2

    bottom_frame = customtkinter.CTkFrame(master=root, fg_color="transparent")

    titlepady = 0
    paramspady = 12
    frame_welcome = customtkinter.CTkFrame(master=root, fg_color="transparent")
    frame_intro = customtkinter.CTkFrame(master=root, fg_color="transparent")
    frame_sessionID = customtkinter.CTkFrame(master=root, fg_color="transparent")
    frame_dates = customtkinter.CTkFrame(master=root, fg_color="transparent")
    frame_directory = customtkinter.CTkFrame(master=root, fg_color="transparent")
    frame_confirm = customtkinter.CTkFrame(master=root, fg_color="transparent")
    frame_result = customtkinter.CTkFrame(master=root, fg_color="transparent")

    frames = [frame_intro, frame_sessionID, frame_dates, frame_directory, frame_confirm]

    b_prev = customtkinter.CTkButton(master = bottom_frame, text = " < Previous ", width=90,
                                             border_color = border_color, border_width=border_width, fg_color="transparent",
                                             command=lambda: prev_frame(frames, b_next, b_prev))

    b_next = customtkinter.CTkButton(master = bottom_frame, text = " Next > ", width=90,
                                             border_color = border_color, border_width=border_width, fg_color="transparent",
                                             command=lambda: next_frame(frames, b_next, b_prev))

    b_next.grid(row=0,column=1, padx=10)


    frame_welcome.pack(expand=True)
    frame_dates.grid_columnconfigure(0, weight=1)
    frame_dates.grid_columnconfigure(1, weight=1)

    welcome = customtkinter.CTkLabel(master=frame_welcome, text="Welcome to\nUPF Calendar Exporter!", font=("Calibri", 30))
    welcome.pack(pady=20, padx=10)

    start = customtkinter.CTkButton(master = frame_welcome, text = "Start", font=("Calibri", 40), width=200, height=100, 
                                             border_color = border_color, border_width=border_width, fg_color="transparent",
                                             command= lambda: frame_start(frame_welcome, frame_intro, bottom_frame))
    start.pack(pady=10, padx=10)

    projectby = customtkinter.CTkLabel(master=frame_welcome, text="a project by @miquelvir", font=("Calibri", 16))
    projectby.pack(pady=20, padx=10)



    login_desc = customtkinter.CTkLabel(master=frame_intro, text="Start by logging in to Secretaria Virtual\nThen click \"Horaris de Classe\"\nThen click \"Veure Calendari\"", font=("Calibri", 24))
    login_desc.pack(pady=12, padx=10)

    open_secretaria = customtkinter.CTkButton(master = frame_intro, text = "Open Secretaria Virtual", font=("Calibri", 16), width=220, height=40, 
                                             border_color = border_color, border_width=border_width, fg_color="transparent",
                                             command=launch_campus_global)
    open_secretaria.pack(pady=20, padx=10)

    _sessionID_title = customtkinter.CTkLabel(master=frame_sessionID, text="Now paste here the JSESSIONID", font=("Calibri", 24))
    _sessionID_title.pack(pady=titlepady, padx=10)
    
    _JSESSIONID = customtkinter.CTkEntry(master=frame_sessionID, placeholder_text="JSESSIONID", width=400)
    _JSESSIONID.pack(pady=12, padx=10)

    jsession_title = customtkinter.CTkLabel(master=frame_sessionID, text="You can find the JSESSIONID doing the following steps:", font=("Calibri", 20))
    jsession_title.pack(pady=4, padx=10)

    tabs = customtkinter.CTkTabview(master=frame_sessionID, border_width=2, height=120)
    tabs.pack(pady=0, padx=10)

    tabs.add("Chrome")
    tabs.add("Firefox")

    jsession_desc_chrome = customtkinter.CTkLabel(master=tabs.tab("Chrome"), text="Right click and select Inspect\nSelect the Application tab\nExpand the Cookies tab", font=("Calibri", 16))
    jsession_desc_chrome.pack(pady=0, padx=0)

    jsession_desc_firefox = customtkinter.CTkLabel(master=tabs.tab("Firefox"), text="Right click and select Inspect Element\nSelect the Storage tab\nExpand the Cookies tab", font=("Calibri", 16))
    jsession_desc_firefox.pack(pady=0, padx=0)

    _dates_desc = customtkinter.CTkLabel(master=frame_dates, text="Select the desired dates to export", font=("Calibri", 24))
    _dates_desc.grid(row= 2,column=0, columnspan=2, pady=12, padx=10)

    _dates_select_start = customtkinter.CTkLabel(master=frame_dates, text="Select the start date", font=("Calibri", 16))
    _dates_select_start.grid(row= 3,column=0,columnspan=1, pady=0, padx=10)
    _dates_select_end = customtkinter.CTkLabel(master=frame_dates, text="Select the end date", font=("Calibri", 16))
    _dates_select_end.grid(row= 3,column=1,columnspan=1, pady=0, padx=10)

    start_cal = Calendar(master=frame_dates, selectmode='day', font=("Calibri", 10),
                        showweeknumbers=False, cursor="hand2", date_pattern= 'y-mm-dd',
                        borderwidth=0, bordercolor='white')
    start_cal.grid(row= 4,column=0, pady=12, padx=10)
    end_cal = Calendar(master=frame_dates, selectmode='day', font=("Calibri", 10),
                        showweeknumbers=False, cursor="hand2", date_pattern= 'y-mm-dd',
                        borderwidth=0, bordercolor='white')
    end_cal.grid(row= 4,column=1, pady=12, padx=10)

    _directory_blank = customtkinter.CTkLabel(master=frame_directory, text="", font=("Calibri", 3))
    _directory_blank.pack(pady=0, padx=10)

    _directory_desc = customtkinter.CTkLabel(master=frame_directory, text="To which directory do you want to export?", font=("Calibri", 24))
    _directory_desc.pack(pady=3, padx=10)

    _directory_ask = customtkinter.CTkEntry(master=frame_directory, placeholder_text="leave empty to generate in this folder", width=400)
    _directory_ask.pack(pady=3, padx=10)


    _directory_separated = customtkinter.CTkCheckBox(master=frame_directory, text="Do you want to export the subjects into different files?",  font=("Calibri", 16), checkmark_color="#000000", fg_color=border_color)
    _directory_separated.pack(pady=28, padx=10)
    
    confirm_text = customtkinter.CTkLabel(master=frame_confirm, text="Click continue to create the calendar", font=("Calibri", 24))
    confirm_text.pack(pady=0, padx=10)

    confirm_text = customtkinter.CTkLabel(master=frame_confirm, text="Click previous to re-check if everything is correct", font=("Calibri", 16))
    confirm_text.pack(pady=0, padx=10)

    confirm = customtkinter.CTkButton(master = frame_confirm, text = "Confirm", font=("Calibri", 40), width=200, height=100, 
                                             border_color = border_color, border_width=border_width, fg_color="transparent",
                                             command= lambda: process_gui(_JSESSIONID.get(), 
                                                                      datetime.strptime(start_cal.get_date(), "%Y-%m-%d"), 
                                                                      datetime.strptime(end_cal.get_date(), "%Y-%m-%d"), 
                                                                      _directory_ask.get(), _directory_separated.get(), frame_result, [bottom_frame, frame_confirm]))
    confirm.pack(pady=30, padx=10)


    


    
    
    

def main():
    print("""
    
    a project by @miquelvir
    ***********************
    
    """)

    root = customtkinter.CTk()
    # root.geometry("620x420")
    root.geometry("700x420")
    # create frame1
    frame_1 = customtkinter.CTkFrame(master=root)
    frame_1.pack(pady=20, padx=60, fill="both", expand=True)
    frame_1.pack()
    frame_config(frame_1, root)

    root.mainloop()


    # print("this script will help you export your UPF Calendar to Google Calendar (or similar)")
    # print_separator()

    # jsessionid, first_date, last_date, saving_path, separate = guide_user_start()
    # print_separator()

    # status = process(jsessionid, first_date, last_date, saving_path, separate)
    # print_separator()

    # if status:
    #     guide_user_end()
    # else:
    #     print("error during the process, troubleshooting steps below")
    #     show_troubleshooting_steps()
    # print_separator()

    # input("enter to exit...")


if __name__ == "__main__":
    main()
