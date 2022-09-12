# database.py
print("This is the database.py module.")
print("Python thinks this is called {}".format(__name__))

from blood_calculator import *

answer = check_HDL(55)
print("The HDL of 55 is {}".format(answer))

answer = check_LDL(55)

