import base64
import io
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from idlelib.tooltip import Hovertip
from PIL import Image, ImageTk
import requests
from datetime import datetime
from final_patient_monitor_server import *
from matplotlib import image as mpimg

url = 'http://127.0.0.1:5000'


def sort_history_dict(history_dict):
    date_time_dict = {}
    for date_time_str, data in history_dict.items():
        date_time_dict[datetime.strptime(date_time_str, '%Y-%m-%d '
                                                        '%H:%M:%S')] = \
            data

    sorted_date_time_dict = dict(sorted(date_time_dict.items()))  # All the
    # keys in this dict will be datetime object

    sorted_date_time_dict_out = {}
    for date_time_obj, data in sorted_date_time_dict.items():
        sorted_date_time_dict_out[date_time_obj.strftime('%Y-%m-%d '
                                                         '%H:%M:%S')] = \
            data
    # Now all the keys in sorted_date_time_dict_out are str from the
    # corresponding datetime object following the format of "%Y-%m-%d %H:%M:%S"
    return sorted_date_time_dict_out


def latest_value_in_history_dict(history_dict):
    sorted_history_dict = sort_history_dict(history_dict)
    latest_value = list(sorted_history_dict.values())[-1]
    return latest_value


def latest_timestamp_in_history_dict(history_dict):
    sorted_history_dict = sort_history_dict(history_dict)
    latest_timestamp = list(sorted_history_dict.keys())[-1]
    return latest_timestamp


def main_window():
    root = tk.Tk()
    root.title("Add-on GUI")

    # ttk.Label(root,text="Patient").grid(column=0,
    #                                   #row=0,
    #                                   #columnspan=2)

    # def ECG_cmd():
    #   root2 = tk.Tk()
    #   root2.title("ECG image")
    #   print(pat)
    #   name = pat_name.get()
    #   ttk.Label(root, text=name).grid(column=0,
    #                                   #row=0)
    #   root2.mainloop

    def openNewWindow():

        #   Toplevel object which will
        #   be treated as a new window
        newWindow = Toplevel(root)

        #   sets the title of the
        #   Toplevel widget
        newWindow.title("New Window")
        #   print(pat['medical_record_number'])
        #   sets the geometry of toplevel
        newWindow.geometry("200x200")

        #   A Label widget to show in toplevel
        Label(newWindow,
              text="Hi").pack()

    # newWindow = Toplevel(root)

    def get_all_med_number():
        #  Professor mentioned that functions like this do not need unit test
        #  functions since it simply obtains data from the server's database
        r = requests.get(url + '/api/monitor/all_med_number')
        if r.status_code == 200:
            all_med_number_list = r.json()
        else:
            all_med_number_list = [
                '(Server database is empty. Have at least 1 patient entry to '
                'proceed.)']
        return all_med_number_list

    def get_patient_data(record_number):
        #  # Professor mentioned that functions like this do not need unit test
        #  # functions since it simply obtains data from the server's database
        r = requests.get(
            url + '/api/monitor/patient_info/{}'.format(record_number))
        if r.status_code == 200:
            patient_info_dict = r.json()
        else:
            patient_info_dict = {}
            messagebox.showwarning('Warning',
                                   'Patient information not found by the '
                                   'given medical record number.')

        return patient_info_dict

    all_med_list = get_all_med_number()

    Label(root, text="med_rec_no").grid(column=0,
                                        row=0,
                                        columnspan=2)
    Label(root, text="patient_name").grid(column=5,
                                          row=0,
                                          columnspan=2)
    Label(root, text="latest_hr").grid(column=10,
                                       row=0,
                                       columnspan=2)
    # a = 10
    for i, rec_no in enumerate(all_med_list):
        pat = get_patient_data(rec_no)
        if len(pat['heart_rate_history']) == 0:
            lat_hr = "no hr"
        else:
            sorted_hr = sort_history_dict(pat['heart_rate_history'])
            lat_hr = latest_value_in_history_dict(sorted_hr)
        # print(pat)
        if pat['patient_name'] is None:
            pat['patient_name'] = "<no name>"
        Label(root, text=pat['patient_name']).grid(column=5,
                                                   row=i+1,
                                                   columnspan=2)
        Label(root, text=pat['medical_record_number']).grid(column=0,
                                                            row=i+1,
                                                            columnspan=2)
        Label(root, text=lat_hr).grid(column=10,
                                      row=i+1,
                                      columnspan=2)

        Button(root, text="ECG", command=openNewWindow).grid(column=15,
                                                             row=i+1,
                                                             columnspan=2)
    root.mainloop()
    # pat1 = get_patient_data(10)
    # sorted_hr_dict = sort_history_dict(pat1['heart_rate_history'])
    # latest_hr = latest_value_in_history_dict(sorted_hr_dict)
    # latest_time = latest_timestamp_in_history_dict(sorted_hr_dict)
    # print(latest_time)
    # print(latest_hr)
    return 0


if __name__ == '__main__':
    main_window()
