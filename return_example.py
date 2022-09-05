def increment_by_five(x):
    a = x + 5
    if x < 0:
        return "This function cannot work on negative numbers"
    return a
    
 
answer = increment_by_five(11)

print("The answer is {}".format(answer))
