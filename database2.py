def create_patient_entry(patient_name, patient_id, patient_age):
    new_patient = [patient_name, patient_id, patient_age, []]
    return new_patient


def main():
    x = create_patient_entry("Ann Ables", 1, 30)
    y = create_patient_entry("Bob Boyles", 2, 34)
    z = create_patient_entry("Chris Chou", 3, 25)
    print(x)


if __name__ == "__main__":
    main()
