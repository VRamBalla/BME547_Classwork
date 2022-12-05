from database_definition import Patient
from pymodm import connect
from flask import Flask, request, jsonify
from pymodm import errors as pymodm_errors
import pandas as pd
from datetime import datetime

app = Flask(__name__)


@app.route('/', methods=['GET'])
def server_on():
    return 'Server is on'


def init_database():
    # This will be commented out eventually. This function doesn't need a
    # unit test but need docstring
    connect(
        'mongodb+srv://davidhe:Davidhe1998@cluster0.grsdcun.mongodb.net'
        '/rb_dataset'
        '?retryWrites=true&w=majority')  # Connect to dummy_dataset
    return 0


# **************************Junqi Lu starts**************************


@app.route('/api/monitor/all_med_number', methods=['GET'])
def get_all_med_number_handler():
    # Since there's no input, this route's handler start from complete tasks
    empty_db_judgement = empty_db_judge()
    all_med_number_list, status = get_all_med_number_worker(
        empty_db_judgement)

    # Return the JSON str and status code back to requestor
    return jsonify(all_med_number_list), status


def get_all_med_number_worker(empty_db_judgement):
    if empty_db_judgement is True:
        return ['Database is empty. Add in data from patient GUI first'], 400
    else:
        med_number_list = []
        for patient in Patient.objects.raw({}):
            med_number = patient.medical_record_number
            med_number_list.append(med_number)

        return med_number_list, 200


def empty_db_judge():
    count = 0
    for patient in Patient.objects.raw({}):
        print(patient)
        count += 1
    if count == 0:
        return True
    else:
        return False


@app.route('/api/monitor/patient_info/<record_number>', methods=['GET'])
def retrieve_patient_info_handler(record_number):
    # No value judgement is needed since record_number is selected by the user
    # from the database (users not allowed to type anything), and we have
    # data validation at the patient
    # GUI to
    # ensure record_number follows the correct data type.

    patient_info_dict, status = retrieve_patient_info_worker(record_number)

    # Return the JSON str and status code back to requestor
    return jsonify(patient_info_dict), status


def retrieve_patient_info_worker(record_number):
    record_number = int(record_number)
    patient_info_dict = {}
    try:
        for patient in Patient.objects.raw({'_id': record_number}):
            patient_info_dict[
                'medical_record_number'] = patient.medical_record_number
            patient_info_dict[
                'patient_name'] = patient.patient_name
            patient_info_dict[
                'heart_rate_history'] = patient.heart_rate_history
            patient_info_dict[
                'ecg_image_history'] = patient.ecg_image_history
            patient_info_dict[
                'medical_filename_history'] = patient.medical_filename_history
            patient_info_dict[
                'medical_image_history'] = patient.medical_image_history
    except (Exception,):
        return jsonify('Something is wrong'), 400
    else:
        return patient_info_dict, 200


# **************************Junqi Lu ends**************************

# **************************Ramana Balla starts**************************
# **************************Ramana Balla ends**************************

# **************************Ziwei He starts**************************


@app.route("/patient_GUI/upload/<warn>", methods=["POST"])
def upload_handler(warn):
    '''Upload patient information handler

    Accept patient information upload. The patient information should be
    formatted as below:
        {
            "patient_record_no": <int> (mandatory)
            "patient_name": <str> (blank if not provide)
            "medical_img": <b64str> (blank if not provide)
            "img_filename": <str> (blank if not provide)
            "ECG_img": <b64str> (blank if not provide)
            "heart_rate": <str> (blank if not provide)
        }
    The <warn> parameter indicates if the user wants to overwrite data. "true"
    means overwrite. Otherwise, the parameter is "false"

    Args:
        warn (string): "true" if the user confirms overwriting. Otherwise, it
        is "false"

    Returns:
        msg (string): Status message.
        status (int): status code.

    '''
    in_data = request.get_json()
    msg, status = info_process(in_data, warn)
    return msg, status


def info_process(in_data, warn):
    '''Process the patient information and return the result of processing.

    This function checks for the existing information of a record number in the
    database. If no record found, the information will be stored in the
    database. If there is existing record, this function updates the record
    unless the name in the record is different from the one provided by the
    user. Confirmation of the user is required to update the name in the
    database.

    Args:
        in_data (dictionary): Patient information in the format of:
            {
                "patient_record_no": <int> (mandatory),
                "patient_name": <str> (blank if not provide),
                "medical_img": <b64str> (blank if not provide),
                "img_filename": <str> (blank if not provide),
                "ECG_img": <b64str> (blank if not provide),
                "heart_rate": <str> (blank if not provide),
            }
        warn (string): "true" if the user confirms overwriting. Otherwise, it
        is "false"

    Returns:
        msg (string): Status message.
        status (int): status code.

    '''
    if warn == "false":
        try:
            x = Patient.objects.raw({"_id": in_data["patient_record_no"]}).\
                first()
            if x.patient_name != in_data["patient_name"]:
                if x.patient_name is not None and \
                        in_data["patient_name"] != '':
                    msg = "Need confirmation for overwriting old name"
                    status = 200
                    return msg, status
                else:
                    save_info(in_data, False)
                    status = 201
                    if [in_data["patient_name"], in_data["ECG_img"],
                            in_data["medical_img"]] == ['', '', '']:
                        msg = "No information need to be updated"
                    else:
                        msg = "Successfully update the information of " +\
                            "patient {}".format(in_data["patient_record_no"])
                    return msg, status
            else:
                save_info(in_data, False)
                if [in_data["ECG_img"], in_data["medical_img"]] ==\
                        ['', '']:
                    msg = "No information need to be updated"
                else:
                    msg = "Successfully update the information of patient {}".\
                        format(in_data["patient_record_no"])
                status = 201
                return msg, status
        except pymodm_errors.DoesNotExist:
            save_info(in_data, True)
            msg = "Successfully upload the patient information"
            status = 201
            return msg, status
    else:
        save_info(in_data, False)
        if in_data["medical_img"] == '' and in_data["ECG_img"] == '':
            msg = "Name updated"
        else:
            msg = "Successfully update the information of patient {}".\
                format(in_data["patient_record_no"])
        status = 201
        return msg, status


def save_info(in_data, first_record):
    '''Save information in the database.

    This function creates new entry in the database and updates existing entry
    based on the uploaded information

    Args:
        in_data (dictionary): Patient information in the format of:
            {
                "patient_record_no": <int> (mandatory),
                "patient_name": <str> (blank if not provide),
                "medical_img": <b64str> (blank if not provide),
                "img_filename": <str> (blank if not provide),
                "ECG_img": <b64str> (blank if not provide),
                "heart_rate": <str> (blank if not provide),
            }
        first_record (boolean): True if there is no existing record in the
        database for the uploaded information. False if there is existing
        record for the uploaded information.

    Returns:
        None.

    '''
    query = Patient.objects.raw({"_id": in_data["patient_record_no"]})
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if first_record:
        info = Patient(medical_record_number=in_data["patient_record_no"])
        if in_data["patient_name"] != '':
            info.patient_name = in_data["patient_name"]
        if in_data["medical_img"] != '':
            medical_img = {timestamp: in_data["medical_img"]}
            img_name = {timestamp: in_data["img_filename"]}
            info.medical_filename_history = img_name
            info.medical_image_history = medical_img
        if in_data["ECG_img"] != '':
            ECG = {timestamp: in_data["ECG_img"]}
            hr = {timestamp: int(in_data["heart_rate"])}
            info.ecg_image_history = ECG
            info.heart_rate_history = hr
        info.save()

    else:
        if in_data["patient_name"] != '':
            query.update({"$set": {"patient_name": in_data["patient_name"]}})
        if in_data["medical_img"] != '':
            query.update({"$set": {"medical_image_history.{}".
                                   format(timestamp): in_data["medical_img"]}})
            query.update({"$set": {"medical_filename_history.{}".
                                   format(timestamp):
                                   in_data["img_filename"]}})
        if in_data["ECG_img"] != '':
            query.update({"$set": {"ecg_image_history.{}".format(timestamp):
                                   in_data["ECG_img"]}})
            query.update({"$set": {"heart_rate_history.{}".format(timestamp):
                                   int(in_data["heart_rate"])}})
# **************************Ziwei He ends**************************


# def main():
#     connect("mongodb+srv://davidhe:Davidhe1998@cluster0.grsdcun.mongodb.net/"
#             "Final_project?retryWrites=true&w=majority")
#     return 0


if __name__ == '__main__':
    init_database()
    # app.run(host="0.0.0.0")  # Remote server
    app.run()  # Local server
