def create_patient_entry(patient_name, patient_id, patient_age):
    new_patient = [patient_name, patient_id, patient_age, []]
    return new_patient

def output(db):
    for x in db:
        print(x)
        print("Name: {}, ID: {}, Age: {} \n".format(x[0],x[1],x[2]))

def search_db(db,id):
    for x in db:
        if x[1] == id:
            return x
    return False

def add_test_results(db,id,test_name,test_value):
    patient = search_db(db,id)
    patient[3].append([test_name,test_value])
    
   
def main():
    db = []
    db.append(create_patient_entry("Ann Ables", 1, 30))
    db.append(create_patient_entry("Bob Boyles", 2, 34))
    db.append(create_patient_entry("Chris Chou", 3, 25))
    add_test_results(db,2,"HDL",100)
    print(search_db(db,2))
    
    room_list = ["Room 1", "Room 2", "Room 3"]
    
    for i, patient in enumerate(db):
        print(i)
        print("Name = {}, Room = {}".format(patient[0],room_list[i]))
    
    for patient, room in zip(db,room_list):
        print("Name = {}, Room = {}".format(patient[0],room))
  
if __name__ == "__main__":
    main()