import requests

r = requests.get("http://vcm-7631.vm.duke.edu:5002/get_patients/vrb12")
print(r.status_code)
print(r.text)

btype_d = requests.get("http://vcm-7631.vm.duke.edu:5002/get_blood_type/F8")
print(btype_d.status_code)
print(btype_d.text)

btype_r = requests.get("http://vcm-7631.vm.duke.edu:5002/get_blood_type/F5")
print(btype_r.status_code)
print(btype_r.text)

out_data = {"Name": "vrb12", "Match": "No"}
r = requests.post("http://vcm-7631.vm.duke.edu:5002/match_check",
                  json=out_data)
print(r.status_code)
print(r.text)
