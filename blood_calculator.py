def interface():
    print("Blood Calculator")
    print("Options")
    print("1 - Analyze HDL")
    print("2 - Analyze LDL")
    print("9 - Quit")
    keep_running = True
    while keep_running:
        choice = input("Enter your choice: ")
        if choice == '9':
            return
        elif choice == '1':
            HDL_driver()
        elif choice == '2':
            LDL_driver()
            
        
def input_HDL():
    HDL_input = input("Enter the HDL value:")
    return int(HDL_input)

def check_HDL(x):
    if x >= 60:
        return "Normal"
    elif 40<= x < 60:
        return "Borderline Low"
    else:
        return "Low"
        
def HDL_driver():
    hdl_value = input_HDL()
    answer = check_HDL(hdl_value)
    output_HDL_result(hdl_value, answer)
    
def output_HDL_result(hdl_value, charac):
    print("The results for an HDL value of {} is {}".format(hdl_value, charac))
    
def input_LDL():
    LDL_input = input("Enter the LDL value:")
    return int(LDL_input)

def check_LDL(y):
    if y >= 190:
        return "Very High"
    elif 160 <= y <= 189:
        return "High"
    elif 130 <= y <= 159:
        return "Borderline high"
    else:
        return "Normal"
        
def LDL_driver():
    ldl_value = input_LDL()
    answer1 = check_LDL(ldl_value)
    output_LDL_result(ldl_value, answer1)
    
def output_LDL_result(ldl_value, charac1):
    print("The results for an LDL value of {} is {}".format(ldl_value, charac1))
    

interface()

