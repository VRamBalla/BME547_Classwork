import requests

output_info = {"user": "Sree",
               "message": "Hi Sree"}

r = requests.post("http://vcm-21170.vm.duke.edu:5001/add_message",
                  json=output_info)
print(r)
print(r.text)

r1 = requests.get("http://vcm-21170.vm.duke.edu:5001/get_messages/vrb12")
print(r1.text)
