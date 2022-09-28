class Patient:

    def __init__(self, first_name, last_name, patient_id, age):
        self.first_name = first_name
        self.last_name = last_name
        self.patient_id = patient_id
        self.age = age
        self.tests = []


def full_name(self):
    return "{} {}".format(self.first_name, self.last_name)


def create_patient_entry(patient_first_name,
                         patient_last_name,
                         patient_id,
                         patient_age):
    new_patient = Patient(patient_first_name,
                          patient_last_name, patient_id,
                          patient_age)
    return new_patient


def output(db):
    for patient_key in db:
        print(patient_key)
        print("Name: {}, ID: {}, Age: {} \n"
              .format(get_full_name(db[patient_key]),
                      db[patient_key]["ID"],
                      db[patient_key]["Age"]))

    for patient_key, patient in zip(db.keys(), db.values()):
        print(patient_key)
        print("Name: {}, ID: {}, Age: {} \n".format(get_full_name(patient),
                                                    patient["ID"],
                                                    patient["Age"]))


def get_full_name(patient):
    full_name = "{} {}".format(patient["First Name"], patient["Last Name"])
    return full_name


def search_db(db, id_no):
    patient = db[id_no]
    return patient


def add_test_results(db, id_no, test_name, test_value):
    patient = search_db(db, id_no)
    patient["Tests"].append([test_name, test_value])


def adult_or_minor(patient):
    if patient["Age"] >= 18:
        return "adult"
    else:
        return "minor"


def main():
    x = Patient("Ramana", "Balla", "", "")
    x.first_name = "Ramana"
    x.last_name = "Balla"
    print(x.full_name())
    exit()

    db = {}
    db[11] = create_patient_entry("Ann", "Ables", 11, 30)
    db[22] = create_patient_entry("Bob", "Boyles", 22, 34)
    db[3] = create_patient_entry("Chris", "Chou", 3, 25)
    output(db)
    add_test_results(db, 3, "HDL", 100)
    output(db)
# print("Patient {} is a {}".format(get_full_name(db[2]),
#                                 adult_or_minor(db[2])))


if __name__ == "__main__":
    main()
